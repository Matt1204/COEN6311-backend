from flask import jsonify, make_response, request, Flask
from ...config import get_db_connection

import pymysql.cursors
import pymysql
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict
import json
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_schedule(data):
    start_date = data.get("start_date")
    if not start_date:
        return (
            jsonify(
                {
                    "error": "server-side issue",
                    "message": "start_date not provided",
                }
            ),
            400,
        )

    conn = get_db_connection()
    
    if conn is None:
        return (
            jsonify(
                {
                    "error": "internal error",
                    "message": "Couldn't connect to the database",
                }
            ),
            500,
        )

    
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    # make sure this start_date is a Monday
    if start_date.weekday() != 0:
        conn.close()
        return jsonify({"message": "Start date must be a Monday"}), 200

    # make sure the schedule for this start_date doesn't already exist
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM master_schedule WHERE shift_date BETWEEN %s AND %s
        """, (start_date, start_date + timedelta(days=6)))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return jsonify({"message": "Schedule already generated for the week"}), 200
    
    shifts, nurses = fetch_data_for_week(start_date, conn)
    shift_ranking_of_nurses = create_rankings(nurses, shifts)
    shift_with_assigned_nurses = deferred_acceptance_matching(nurses, shifts)
    master_schedule = create_master_schedule(shift_with_assigned_nurses, shifts)
    save_master_schedule(master_schedule, conn)

    conn.close()

    return jsonify({"message": "Schedule generated successfully"}), 200    

class Nurse:
    def __init__(self, id, seniority, shift_type, hours_per_week, preferred_days, max_hours_per_shift, hospitals_ranking):
        self.id = id
        self.seniority = seniority
        self.shift_type = shift_type
        self.hours_per_week = hours_per_week
        self.preferred_days = preferred_days
        self.max_hours_per_shift = max_hours_per_shift
        self.hospitals_ranking = hospitals_ranking
        self.capacity = hours_per_week // 8  # Maximum number of shifts a nurse can work in a week (Assuming 8 hours per shift)
        self.remaining_weekly_hours = hours_per_week  # Initialize remaining weekly hours

        self.shift_rankings = []  # Will be populated by ranking algorithm
        self.assigned_shifts = set()
    
    def __repr__(self):
        # print all nurse's information including preferences
        return f"Nurse ID: {self.id}, Seniority: {self.seniority}, Shift Type: {self.shift_type}, Hours Per Week: {self.hours_per_week}, Preferred Days: {self.preferred_days}, Max Hours Per Shift: {self.max_hours_per_shift}, Hospitals Ranking: {self.hospitals_ranking}"

    def reject_shifts(self):
        '''
        Trim the self.assigned_shifts set down to its capacity, returning the removed shifts
        '''
        if len(self.assigned_shifts) <= self.capacity:
            return set()
        else:
            # sort the list of assigned shifts by nurse's preferences
            # this is to keep the nurse's best preferred shifts (at each iteration)
            sorted_assigned_shifts = sorted(list(self.assigned_shifts), key=lambda shift: self.shift_rankings.index(shift.id))

            # check for overlapping shifts and remove the ones with the lowest preference
            non_overlapping_shifts = []
            rejected_overlapping_shifts = []
            for shift in sorted_assigned_shifts:
                if not any(s.shift_date == shift.shift_date and s.shift_type == shift.shift_type for s in non_overlapping_shifts):
                    non_overlapping_shifts.append(shift)
                else:
                    rejected_overlapping_shifts.append(shift)
                
            
            self.assigned_shifts = set(non_overlapping_shifts[:self.capacity])
            return set(non_overlapping_shifts[self.capacity:] + rejected_overlapping_shifts) 

class Shift:
    def __init__(self, id, hospital_id, supervisor_id, shift_type, hours_per_shift, day_of_week, number_of_nurses, min_seniority, shift_date):
        self.id = id
        self.hospital_id = hospital_id
        self.supervisor_id = supervisor_id
        self.shift_type = shift_type
        self.hours_per_shift = hours_per_shift
        self.day_of_week = day_of_week
        self.capacity = number_of_nurses
        self.min_seniority = min_seniority
        self.shift_date = shift_date

        self.nurse_rankings = []  # Will be populated by ranking algorithm
        self.assigned_nurses = set()
        self.min_nurses = 2 # Minimum number of nurses required for a shift
        self.proposals = 0  # Number of proposals made to nurses

    def __repr__(self):
        # print all shift's information including rqeuirements
        return f"Shift ID: {self.id}, Hospital ID: {self.hospital_id}, Shift Type: {self.shift_type}, Hours Per Shift: {self.hours_per_shift}, Day of Week: {self.day_of_week}, Number of Nurses: {self.capacity}, Min Seniority: {self.min_seniority}, Shift Date: {self.shift_date}"
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def next_preferred_nurse(self):
        return self.nurse_rankings[self.proposals]
    
    def is_properly_staffed(self) -> bool:
        '''Check if the shift has enough nurses assigned'''
        return len(self.assigned_nurses) >= self.min_nurses
        
    def can_accept_more_nurses(self):
        return len(self.assigned_nurses) < self.capacity

def fetch_data_for_week(start_date: datetime, conn):
    """Fetch all relevant data for a week's schedule"""
    shifts: List[Shift] = []
    nurses: List[Nurse] = []

    try:
        with conn.cursor() as cursor:
            # Fetch shifts
            cursor.execute("""
                SELECT request_id, hospital_id, supervisor_id, shift_type, min_seniority, shift_date, 
                    hours_per_shift, nurse_number, day_of_week
                FROM shift_request 
                WHERE shift_date BETWEEN %s AND %s
            """, (start_date, start_date + timedelta(days=6)))
            
            shift_columns = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
                shift_data = dict(zip(shift_columns, row))
                shifts.append(Shift(
                    id=shift_data['request_id'],
                    hospital_id=shift_data['hospital_id'],
                    supervisor_id=shift_data['supervisor_id'],
                    shift_type=shift_data['shift_type'],
                    hours_per_shift=shift_data['hours_per_shift'],
                    day_of_week=shift_data['day_of_week'],
                    number_of_nurses=shift_data['nurse_number'],
                    min_seniority=shift_data['min_seniority'],
                    shift_date=shift_data['shift_date']
                ))
            
            # Fetch nurses and their preferences
            cursor.execute("""
                SELECT n.u_id, n.seniority, p.time_of_day, p.hours_per_week,
                    p.preferred_week_days, p.max_hours_per_shift, p.hospitals_ranking
                FROM user n
                JOIN shift_preference p ON n.u_id = p.nurse_id and n.role = 'nurse'
            """)
            nurse_columns = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
                nurse_data = dict(zip(nurse_columns, row))
                hospitals_ranking = json.loads(nurse_data['hospitals_ranking'])
                
                # change hospitals ranking into a dictionary with hospital id as key and ranking as value
                hospitals_ranking = {k: v+1 for v, k in enumerate(hospitals_ranking)}

                nurses.append(Nurse(
                    id=nurse_data['u_id'],
                    seniority=nurse_data['seniority'],
                    shift_type=nurse_data['time_of_day'],
                    hours_per_week=nurse_data['hours_per_week'],
                    preferred_days=json.loads(nurse_data['preferred_week_days']),
                    max_hours_per_shift=nurse_data['max_hours_per_shift'],
                    hospitals_ranking=hospitals_ranking
                ))
    except Exception as e:
        logging.error(f"Error fetching data for schedule: {e}")
        return [], []
    return shifts, nurses

def calculate_nurse_shift_score(nurse, shift):
    """Calculate how well a shift matches a nurse's preferences"""
    score = 0.0
    
    # Time of day preference
    # We can add a feature where a nurse can indicate how important this preference is (from 1 to 3 or something like that to aid with the score calculation)
    if shift.shift_type == nurse.shift_type:
        score += 1
    
    # Preferred weekdays
    preferred_days = nurse.preferred_days
    if shift.day_of_week in preferred_days:
        score += 1
        
    # Hours per shift preference
    if shift.hours_per_shift <= nurse.max_hours_per_shift:
        score += 1

    # penalize if the shift min_seniority is higher than the nurse's seniority
    if shift.min_seniority > nurse.seniority:
        score -= 1

    # penalize if the shift min_seniority is much less than the nurse's seniority
    if shift.min_seniority < nurse.seniority - 3:
        score -= 1
        
    # Hospital preference
    hospitals_ranking = nurse.hospitals_ranking
    hospital_rank = hospitals_ranking[shift.hospital_id]
    score += 1 / hospital_rank
    
    return score

def calculate_shift_nurse_score(shift, nurse):
    """Calculate how well a nurse matches a shift's requirements"""
    score = 0.0
    
    # # Seniority requirement
    # seniority_levels = {'junior': 1, 'mid': 2, 'senior': 3}
    # required_seniority = seniority_levels[shift.min_seniority]
    # nurse_seniority = seniority_levels[nurse.seniority]
    
    if nurse.seniority >= shift.min_seniority:
        score += nurse.seniority - shift.min_seniority + 1  # Bonus for higher seniority
        # score += 1
        # if nurse_seniority > required_seniority:
        #     score += (nurse.seniority - 1)  # Bonus for higher seniority
    
    # # Availability for shift hours
    # if shift['HoursPerShift'] <= nurse.preferences['MaxHoursPerShift']:
    #     score += 2
        
    return score

def create_rankings(nurses, shifts):
    """Create rankings for both nurses and shifts"""
    
    # Calculate scores and create rankings for nurses
    for nurse in nurses:
        shift_scores = [(shift.id, calculate_nurse_shift_score(nurse, shift)) 
                       for shift in shifts]
        # Sort by score descending, break ties by shift ID
        nurse.shift_rankings = [shift_id for shift_id, _ in sorted(shift_scores, key=lambda x: (-x[1], x[0]))]
    
    # Calculate scores and create rankings for shifts
    shift_ranking_of_nurses = {}
    for shift in shifts:
        nurse_scores = [(nurse.id, calculate_shift_nurse_score(shift, nurse)) for nurse in nurses]
        
        # Sort by score descending, break ties by nurse ID
        shift.nurse_rankings = [nurse_id for nurse_id, _ in sorted(nurse_scores, key=lambda x: (-x[1], x[0]))]
        shift_ranking_of_nurses[shift.id] = shift.nurse_rankings
    
    return shift_ranking_of_nurses

def deferred_acceptance_matching(nurses, shifts):
    """
    Implement the deferred acceptance algorithm for many-to-many matching
    Returns: Dictionary mapping Nurse IDs to assigned Shift IDs
    """
    
    unassigned = shifts
    # randomize to ensure fairness of order
    random.shuffle(unassigned)
    round_num = 1

    for shift in shifts:
        if len(shift.nurse_rankings) == 0:
            logging.warning(f'Shift {shift.id} has no rankings for nurses and probably didn\'t submit requirements and is removed from the matching process')
            unassigned.remove(shift)

    for nurse in nurses:
        if len(nurse.shift_rankings) == 0:
            logging.warning(f'Nurse {nurse.id} has no rankings for shifts and probably didn\'t submit preferences and is removed from the matching process')
            nurses.remove(nurse)
    

    nurses = {nurse.id: nurse for nurse in nurses}

    while len(unassigned) > 0:
        logging.info(f'Round: {round_num}')
        logging.info(f'Unassigned shifts Remaining: {len(unassigned)}')
        round_num += 1
        
        for shift in unassigned:
            if (len(shift.assigned_nurses) < shift.capacity) and (shift.proposals < len(shift.nurse_rankings)):
                preferred_nurse_id = shift.next_preferred_nurse()
                preferred_nurse = nurses[preferred_nurse_id]
                if shift.id in preferred_nurse.shift_rankings:
                    preferred_nurse.assigned_shifts.add(shift)
                    shift.assigned_nurses.add(preferred_nurse.id)
                shift.proposals += 1

        for nurse in nurses.values():
            # reject existing shifts if a more preferred shift comes along and fills the capacity
            rejected_shifts = nurse.reject_shifts()

            for shift in rejected_shifts:
                # remove nurse from rejected shifts to allow those shifts to potentially match with others
                shift.assigned_nurses.remove(nurse.id)

        # remove from unassigned if shift has proposed to all of its preferred nurses or is shift is at capacity
        removed = [shift for shift in unassigned if (shift.proposals >= len(shift.nurse_rankings)) or (len(shift.assigned_nurses) >= shift.capacity)]

        # update unassigned to smaller set
        unassigned = set(unassigned) - set(removed)
        unassigned = list(unassigned)
        logging.info(f'Unassigned shifts Remaining: {len(unassigned)} After Round')
        random.shuffle(unassigned)

    return {shift.id: shift.assigned_nurses for shift in shifts}

def create_master_schedule(matching_result: Dict[int, set], 
                         shifts: List[dict]) -> List[dict]:
    """Convert matching results to master schedule entries"""
    master_schedule = []
    
    for shift in shifts:
        shift_id = shift['id']
        assigned_nurses = matching_result[shift_id]
        
        for nurse_id in assigned_nurses:
            master_schedule.append({
                'request_id': shift_id,
                'supervisor_id': shift['supervisor_id'],
                'hospital_id': shift['hospital_id'],
                'nurse_id': nurse_id,
                'shift_date': shift['shift_date']
            })
    
    return master_schedule

def save_master_schedule(master_schedule: List[dict], conn):
    """Save the master schedule to the database"""
    try:
        with conn.cursor() as cursor:
            for entry in master_schedule:
                cursor.execute("""
                    INSERT INTO master_schedule (request_id, supervisor_id, hospital_id, nurse_id, shift_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (entry['request_id'], entry['supervisor_id'], entry['hospital_id'], entry['nurse_id'], entry['shift_date']))
            conn.commit()
    except Exception as e:
        logging.error(f"Error saving master schedule: {e}")
