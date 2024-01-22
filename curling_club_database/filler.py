import pandas as pd
import numpy as np
import names #!
from urllib.parse import quote  
from sqlalchemy.engine import create_engine
import random
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import itertools

# Phone
N = 1000
phones_base = random.sample(range(100000000, 999999999+1), N)

# Fillers
class DbFiller:
    def __init__(self, tabtype, N):
        self.tabtype = tabtype
        self.N = N
        self.beginning = date(2000, 4, 20)
    
    def generate_id(self, start):
        return np.arange(start, self.N+1)
    
    def players_names(self):
        females = list(np.zeros(int(self.N/2)))
        males = list(np.zeros(int(self.N/2)))
        for i in range(int(self.N/2)):
            f_name = names.get_first_name(gender="female")
            females[i] = (f_name, "f")
            m_name = names.get_first_name(gender="male")
            males[i] = (m_name, "m")
        mf = males + females
        random.shuffle(mf)
        first_names = [mf[i][0] for i in range(len(mf))]
        gender = [mf[i][1] for i in range(len(mf))]
        return first_names, gender
    
    def last_names(self):
        lastnames = list(np.zeros(self.N))
        for i in range(self.N):
            last = names.get_last_name()
            lastnames[i] = last
        return lastnames
    
    def make_date(self, day, age):
        d = datetime.strptime(str(date.today().year - age) + "-" + str(day), "%Y-%j").strftime("%d-%m-%Y")
        d = datetime.strptime(d, '%d-%m-%Y')
        return datetime.date(d)
    
    def contract_start(self, birth_date):
        start = birth_date + timedelta(days = np.random.randint(1, 366)) + relativedelta(years=14) # mogą się zakontraktować po 14 roku zycia
        end = datetime.date(datetime.today()) - relativedelta(years = 1) # bierzemy do roku poprzedniego, żeby data kontraktu była wcześniejsza niż rozgrywek
        time_between = end - start
        days_between = time_between.days
        random_date = start + timedelta(days = np.random.randint(days_between))
        if random_date < self.beginning:
               random_date = self.beginning
        return random_date
    
    def contract_end(self, start_date):
        status = {"active":0.2, "inactive":0.8}
        status_sample = np.random.choice(list(status.keys()), p=list(status.values()), size=1)
        if status_sample == "active":
            end_date = datetime.date(datetime(9999, 1, 1))
        else:
            start = start_date + timedelta(days = 60) # muszą przepracować minimum 60 dni na kontrakcie
            end = datetime.date(datetime.today())
            time_between = end - start
            days_between = time_between.days
            end_date = start + timedelta(days = np.random.randint(days_between))
        return end_date
    
    def player_contract(self):
        age = np.random.lognormal(0, 0.45, self.N)
        age = 11*age + 17
        age = np.array([min(age[i], 60) for i in range(self.N)])
        age = age.astype(int)
        age_datetime = np.random.randint(1, 366, size=self.N)
        birth = list(np.zeros(self.N))
        start = list(np.zeros(self.N))
        end = list(np.zeros(self.N))
        for i in range(self.N):
            birth[i] = self.make_date(age_datetime[i], age[i])
            start[i] = self.contract_start(birth[i])
            end[i] = self.contract_end(start[i])
        return birth, start, end
    
    def phones_generator(self, start):
        return phones_base[start:self.N+start]
    
    def mail_generator(self, first_name, last_name, birth_date):
        year = str(birth_date.year)[2:4]
        name_firstl = first_name[0]
        last_name_firstl = last_name[0]
        pattern1 = [name_firstl, last_name]
        pattern2 = [first_name, last_name]
        pattern3 = [first_name, last_name_firstl]
        pattern = [pattern1, pattern2, pattern3]
        index = np.random.randint(3)
        pattern = pattern[index]
        random.shuffle(pattern)
        if np.random.randint(2) == 0:
            final_pattern = pattern[0] + pattern[1] + year
        else:
            final_pattern = pattern[0] + pattern[1]
        return final_pattern.lower() + "@giniewicz.it"
    
    def staff_names(self):
        staff_name = list(np.zeros(self.N))
        staff_name[0] = 'Mariusz'
        staff_name[1] = 'Ada'
        staff_name[2] = 'Wojciech'
        staff_name[3] = 'Sebastian'
        staff_name[4] = 'Paweł'
        staff_name[5] = 'Katarzyna'
        for i in range(6, self.N):
            staff_name[i] = names.get_first_name()
        return staff_name
    
    def staff_lastnames(self):
        staff_last_name = self.last_names()
        staff_last_name[0] = 'Olszewski'
        staff_last_name[1] = 'Majchrzak'
        staff_last_name[2] = 'Strycharczyk'
        staff_last_name[3] = 'Janus'
        staff_last_name[4] = 'Kossowski-Skop'
        staff_last_name[5] = 'Macioszek'
        return staff_last_name
    
    def staff_contracts(self):
        staff_positions = ["president"] + ["hr manager"] + ["asset manager"] + ["marketing manager"] \
        + ["equipment manager"] + ["accountant"] + ["ice maker"]*4 + ["physiotherapist"]*8 + ["technical service"]*50 + ["trainer"]*10
        staff_count = {"ice maker":1, "physiotherapist":2, "technical service":10, "trainer":2}
        staff_start_date = list(np.zeros(len(staff_positions)))
        staff_end_date = list(np.zeros(len(staff_positions)))
        i = 0
        club_age = date.today().year - self.beginning.year
        counter = 0
        while i < (len(staff_positions)):
            if i < 6:
                staff_start_date[i] = self.beginning
                staff_end_date[i] = date(9999, 1, 1)
                counter = i + 1
                i += 1
            else:
                amount = staff_positions.count(staff_positions[i])
                employed = staff_count[staff_positions[i]]
                period = np.ceil(club_age*employed/amount)
                for j in range(amount):
                    if j < employed:
                        staff_start_date[i+j] = self.beginning
                        staff_end_date[i+j] = self.beginning + relativedelta(years=np.random.randint(period-1, period+2))
                    else:
                        staff_start_date[i+j] = staff_end_date[i+j-employed] - timedelta(days = 30)
                        staff_end_date[i+j] = staff_start_date[i+j] + relativedelta(years = np.random.randint(period, period+2))
                    counter = i+j
                i = counter + 1
        staff_end_date = [date(9999, 1, 1) if staff_end_date[i] > date.today() else \
                          staff_end_date[i] for i in range(len(staff_end_date))]
        return staff_positions, staff_start_date, staff_end_date
    
    def sponsors_names(self):
        n = datetime.today().year - self.beginning.year
        sponsors = list(np.zeros(n)) 
        sponsor = names.get_last_name() + " Company"
        for i in range(n):
            if np.random.randint(3) == 0:
                sponsor = names.get_last_name() + " Company"
            sponsors[i] = sponsor
        return sponsors
            
    def sponsors_dates(self, sponsors):
        name_sponsor = list(set(sponsors)) # lista wszystkich sponsorów
        n = len(name_sponsor)
        sponsor_mail = list(np.zeros(n))
        for i in range(n):
            sponsor_mail[i] = name_sponsor[i].replace(" ", "_") + "@giniewicz.it"
        len_sponsor = list(np.zeros(n))
        for i in range(n):
            len_sponsor[i] = sponsors.count(name_sponsor[i])
        sponsor_start = list(np.zeros(n))
        sponsor_start[0] = self.beginning
        for i in range(1, n):
            sponsor_start[i] = sponsor_start[i - 1] + relativedelta(years = len_sponsor[i - 1]) + timedelta(days=int(np.random.normal(0, 5)))  
        sponsor_end = list(np.zeros(n))
        for i in range(n):
            sponsor_end[i] = sponsor_start[i] + relativedelta(years = len_sponsor[i])
        sponsor_end[-1] = date(9999, 1, 1)
        return name_sponsor, sponsor_mail, sponsor_start, sponsor_end
    
    def equipment(self):
        club_age = date.today().year - self.beginning.year
        categories = ["broom"]*80 + ["stone"]*160 + ["biter stick"]*6 + ["hack"]*40 \
        + ["micrometer"]*6 + ["nipper"]*2 + ["pebbler"]*6 + ["scoreboard"]*2
        equip_id = np.arange(1, len(categories), 1)
        brands = ["Broom4U"]*80 + ["Dakota Curling Supplies"]*166 + ["Goldline Curling Supplies"]*46 + ["IceMachinezzz"]*11
        brooms = ["Cleansweep", "CometTwoNinety", "Nimbus2000", "Nimbus2001"]
        stones = ["gigastoner", "stoned420", "modernstoner", "dakotastoned"]
        biters = ["biteMe", "biteMe2"]
        hacks = ["OfficerHack", "CaptainHack"]
        micrometers = ["micro00", "micro01"]
        nippers = ["nip", "nipnip"]
        pebblers = ["hotshower00", "hotshower01", "hotshower03"]
        models = brooms*20 + stones*40 + biters*3 + hacks*20 + micrometers*3 + nippers + pebblers*2 + ["FairPlay2000"]
        return pd.DataFrame(list(zip(equip_id, categories, brands, models)), \
                           columns = ["equipment_id", "category", "brand", "model"])
    
    def generate(self):
        if self.tabtype == "player":
            ids = self.generate_id(1)
            firstnames, gender = self.players_names()
            lastnames = self.last_names()
            ages, start, end = self.player_contract()
            phones = self.phones_generator(1)
            mails = list(np.zeros(self.N))
            for i in range(self.N):
                mails[i] = self.mail_generator(firstnames[i], lastnames[i], ages[i])
            return pd.DataFrame(list(zip(ids, firstnames, lastnames, gender, ages, start, end, phones, mails)), \
                               columns = ["player_id", "first_name", "last_name", "gender", "birth_date", "contract_from", \
                                         "contract_to", "phone", "email"])
        elif self.tabtype == "staff":
            ids = self.generate_id(1)
            firstnames = self.staff_names()
            lastnames = self.staff_lastnames()
            position, start, end = self.staff_contracts()
            phones = self.phones_generator(500)
            mails = list(np.zeros(self.N))
            for i in range(self.N):
                mails[i] = self.mail_generator(firstnames[i], lastnames[i], date(2000 + np.random.randint(99), 1, 1))
            return pd.DataFrame(list(zip(ids, firstnames, lastnames, position, start, end, phones, mails)), \
                               columns = ["staff_id", "first_name", "last_name", "position", "hire_date", \
                                         "end_date", "phone", "email"])
        
        elif self.tabtype == "sponsors":
            ids = self.generate_id(1)
            name = self.sponsors_names()
            names, mails, start, end = self.sponsors_dates(name)
            phones = self.phones_generator(700)
            return pd.DataFrame(list(zip(ids, names, start, end, phones, mails)), \
                               columns = ["sponsor_id", "full_name", "contract_from", "contract_to", "phone", "email"])
        
        elif self.tabtype == "equipment":
            eq = self.equipment()
            return(eq)
        
class DbFiller2:
    def __init__(self, players):
        self.players = players
        self.female = players[players['gender'] == 'f'].reset_index(drop=True)
        self.male = players[players['gender'] == 'm'].reset_index(drop=True)
        
    def generate_team(self, team_players, team_id):
        teams_id = list(np.zeros(len(team_players)))
        player_pos = list(np.zeros(len(team_players)))
        positions = ['skip', 'leader', 'second', 'third'] * 2
        iterator = 0
        con_end_list = list(team_players['contract_to'])
        teams_id[0] = team_id
        player_pos[0] = positions[0]
        for i in range(1, len(team_players)):    
            min_date = min(con_end_list[0:i])
            if team_players['contract_from'][i] <= min_date:
                teams_id[i] = team_id
                player_pos[i] = positions[(i - iterator)%8]
                if (i - iterator)%8 == 0:
                    team_id += 1
            else:
                index = con_end_list.index(min_date)
                teams_id[i] = teams_id[index]
                player_pos[i] = player_pos[index]
                con_end_list[index] = date(9999, 1, 1)
                iterator += 1
        return  pd.DataFrame(list(zip(team_players['player_id'], teams_id, player_pos, team_players['contract_from'])), \
                       columns = ['player_id', 'team_id', 'position', 'contract_start'])
    
    def generate(self):
        men = self.generate_team(self.male, 1)
        fmen = self.generate_team(self.female, 100)
        return pd.concat([men, fmen]).reset_index(drop=True)
    
class DbFiller3():
    def __init__(self, teams):
        self.teams = teams
        self.male = teams[teams['team_id']<100]
        self.female = teams[teams['team_id']>=100]
    
    def team_start(self, teams, team_nr, men):
        team_ids = list(np.zeros(team_nr))
        team_year = list(np.zeros(team_nr))
        for i in range(team_nr):
            team_ids[i] = i+1+men
            years = list(teams[teams['team_id']==i+1+men]['contract_start'])
            years.sort()
            try:
                team_year[i] = years[3].year + 1
            except IndexError:
                team_year[i] = date.today().year + 1
        return pd.DataFrame(list(zip(team_ids, team_year)), columns=['team_id', 'start'])
    
    def generate_match(self, match_id):
        probs = (0.35, 0.3, 0.25, 0.05, 0.03, 0.01, 0.005, 0.003, 0.002)
        possible_scores = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        match = []
        teamA_total = 0
        teamB_total = 0
        for end in range(1, 11):
            # Select the scoring team
            team = np.random.randint(1,3)
            # Generate the score
            score = np.random.choice(possible_scores, p=probs)
            if team == 1:
                teamA_score = score
                teamB_score = 0
                teamA_total += score
            else:
                teamA_score = 0
                teamB_score = score
                teamB_total += score
            match.append([match_id, end, teamA_score, teamB_score])
            
            if end >= 7 and abs(teamA_total - teamB_total) >= 5:
                return pd.DataFrame(match, columns=['match_id', 'round_number', 'teamA_score', 'teamB_score'])

        if teamA_total == teamB_total:
            team = np.random.randint(1,3)
            if team == 1:
                match.append([match_id, 11, 1, 0])
            else:
                match.append([match_id, 11, 0, 1])
                
        return pd.DataFrame(match, columns=['match_id', 'round_number', 'teamA_score', 'teamB_score'])
    
    def gen_match(self, df, year):
        teams = list(df[df['start'] <= year.year]['team_id'])
        for i in teams:
            current = self.teams[self.teams["team_id"] == i]
            new_current = list(current[current["contract_to"] < year]["position"])
            if "leader" not in new_current and "skip" not in new_current and "second" not in new_current and "third" not in new_current:
                teams.remove(i)
        n_teams = len(teams)
        if n_teams > 1:
            matches = list(itertools.combinations(teams, 2))
            return random.sample(matches, k = len(matches))
    
    def tournament_gen(self, df):
        match_date = []
        match = []
        year = date(df['start'][1], 1, 7)
        while year < date.today():
            matches = self.gen_match(df, year)
            for i in range(len(matches)):
                match_date.append(year + timedelta(days = i*2))
                match.append(matches[i])
            year = year + relativedelta(years=4)
        return pd.DataFrame(list(zip(match_date, match)), columns=['date', 'teams'])
    
    def generate_matches(self, df, staff, gender):
        genders = {'f':20000, 'm':10000}
        trainers = staff[staff['position']=='trainer']
        matches = list(df['teams'])
        match_id = list(np.zeros(len(matches)))
        match_teamA = list(np.zeros(len(matches)))
        match_teamB = list(np.zeros(len(matches)))
        trainerA = list(np.zeros(len(matches)))
        trainerB = list(np.zeros(len(matches)))
        match_date = list(df['date'])
        for i in range(len(matches)):
            match_id[i] = genders[gender] + i + 1
            match_teamA[i], match_teamB[i] = matches[i]
            available = trainers[trainers['hire_date']<df['date'][i]]
            available = available[available['end_date']>df['date'][i]]
            available = available.reset_index(drop=True)
            trainerA[i], trainerB[i] = available['staff_id'][0], available['staff_id'][1]

        return pd.DataFrame(list(zip(match_id, match_teamA, match_teamB, trainerA, trainerB, match_date)), columns=['match_id', 'teamA', 'teamB', 'trainerA_id', 'trainerB_id', 'match_date'])
    
    
    def generate(self, staff):
        men_team_start = self.team_start(self.male, max(self.male['team_id']), 0)
        fmen_team_start = self.team_start(self.female, max(self.female['team_id'])-100, 100)
        men_matches = self.tournament_gen(men_team_start)
        fmen_matches = self.tournament_gen(fmen_team_start)
        matches1 = self.generate_matches(men_matches, staff, 'm')
        matches2 = self.generate_matches(fmen_matches, staff, 'f')
        matches = pd.concat([matches1, matches2]).reset_index(drop=True)
        match1 = self.generate_match(matches['match_id'][0])
        for i in range(1, len(matches)):
            next_match = self.generate_match(matches['match_id'][i])
            match1 = pd.concat([match1, next_match]).reset_index(drop=True)
        return matches, match1
    
class DbFiller4():
    def __init__(self, sponsors, staff, equipment):
        self.sponsors = sponsors
        self.staff = staff
        self.equipment = equipment
        self.beginning = date(2000, 4, 20)
        
    def transaction_eq(self):
        eq_positions = list(self.equipment['category'])
        eq_count = {"broom":20, "stone":40, "biter stick":2, "hack":10, "micrometer":2, "nipper":1, \
                       "pebbler":2, "scoreboard":1}
        prices = {"broom":100, "stone":12, "biter stick":215, "hack":30, "micrometer":725, "nipper":1700, \
                       "pebbler":250, "scoreboard":800}
        transaction_id = list(np.ones(len(eq_positions), dtype = np.int8))
        buy_date = list(np.zeros(len(eq_positions)))
        expire = list(np.zeros(len(eq_positions)))
        eq_price = list(np.zeros(len(eq_positions)))
        i = 0
        club_age = date.today().year - self.beginning.year
        counter = 0
        while i < (len(eq_positions)):
            amount = eq_positions.count(eq_positions[i])
            equip = eq_count[eq_positions[i]]
            price = prices[eq_positions[i]]
            period = np.ceil(club_age*equip/amount)
            for j in range(amount):
                if j < equip:
                    buy_date[i+j] = self.beginning
                    expire[i+j] = self.beginning + relativedelta(years=np.random.randint(period-1, period+2))
                else:
                    buy_date[i+j] = expire[i+j-equip] - timedelta(days = 30)
                    expire[i+j] = buy_date[i+j] + relativedelta(years = np.random.randint(period, period+2))
                eq_price[i+j] = price
                counter = i+j
            i = counter + 1
        eq_trans = pd.DataFrame(list(zip(self.equipment['equipment_id'], self.equipment['category'], buy_date, eq_price)), \
                            columns = ['equipment_id','category', 'date', 'price'])
        eq_trans1 = eq_trans.sort_values(by=['date', 'category']).reset_index(drop=True)
        iterator = 1
        transaction_id[0] = 10001
        for i in range(1, len(eq_trans)):
            if eq_trans1['category'][i] != eq_trans1['category'][i - 1] or eq_trans1['date'][i] != eq_trans1['date'][i - 1]:
                iterator += 1
            transaction_id[i] = 10000 + iterator
        eq_trans1['transaction_id'] = transaction_id
        return eq_trans1.sort_values(by=['equipment_id']).reset_index(drop=True)
    
    def generate_salaries(self):
        amounts = {"president":50000, "hr manager":5000, "asset manager":5000, "marketing manager":5000, \
                  "equipment manager":5000, "accountant":5000, "ice maker":2000, "physiotherapist":2500, \
                  "technical service":1500, "trainer":2500}
        staff_ids = list(self.staff["staff_id"])
        staff_list = list(self.staff["position"])
        staff_from = list(self.staff["hire_date"])
        staff_to = list(self.staff["end_date"])
        salaries_dates = []
        salaries_amounts = []
        sal_staff_ids = []
        for i in range(len(staff_list)):
            sid = staff_ids[i]
            position = staff_list[i]
            date_from = staff_from[i]
            sal = amounts[position]
            if staff_to[i] == date(9999,1,1):
                date_to = date.today()
            else:
                date_to = staff_to[i]
            salary_date = date_from 
            while salary_date < date_to:
                salary_date = salary_date + relativedelta(months=1)
                salaries_dates.append(salary_date)
                salaries_amounts.append(sal)    
                sal_staff_ids.append(sid)
        salaries = pd.DataFrame(list(zip(salaries_dates, salaries_amounts, sal_staff_ids)), \
                                columns = ["date", "amount", "staff_id"])
        sal_sorted = salaries.sort_values(by = "date").reset_index(drop=True)
        sal_sorted["transaction_id"] = [20000+i for i in range(1, len(sal_sorted)+1)]
        return sal_sorted[["transaction_id", "amount", "date", "staff_id"]]
    
    def sponsors_transactions(self):
        months = (date.today().year - self.beginning.year)*12 + date.today().month - self.beginning.month
        trans = np.zeros(months, dtype=int)
        spons_ids = np.zeros(months, dtype=int)
        trans_ids = [30000+i for i in range(1, months)]
        trans_date = list(np.zeros(months))
        trans_date[0] = self.beginning
        n = len(self.sponsors)
        count = 0
        for j in range(1, months):
            trans_date[j] = trans_date[j-1] + relativedelta(months=1)
        for i in range(n-1):
            timediff = (self.sponsors["contract_to"][i].year - self.sponsors["contract_from"][i].year)*12
            trans[count:(count+timediff)] = np.random.choice([100000, 125000, 95000, 110000])
            spons_ids[count:count+timediff] = self.sponsors["sponsor_id"][i]
            count += timediff
        timediff = (date.today().year - self.sponsors["contract_from"][n-1].year)*12 + \
                         date.today().month - self.sponsors["contract_from"][n-1].month
        trans[count:count+timediff] = np.random.choice([100000, 125000, 95000, 110000])
        spons_ids[count:count+timediff] = self.sponsors["sponsor_id"][n-1]
        return pd.DataFrame(list(zip(trans_ids, spons_ids, trans, trans_date)), \
                            columns=['transaction_id', 'sponsor_id', 'amount', 'date'])
        
class DbFiller5():
    def __init__(self, salaries, expenses, sponsor_trans):
        self.salaries = salaries
        self.expenses = pd.DataFrame(list(zip(expenses['transaction_id'], expenses['price'])), columns=['transaction_id', 'amount'])
        self.sponsors = sponsor_trans
        
    def financials(self):
        eq2 = self.expenses.groupby('transaction_id').sum().reset_index()
        ids = list(self.salaries['transaction_id']) + list(eq2['transaction_id']) + list(self.sponsors['transaction_id'])
        amount = list(self.salaries['amount']) + list(eq2['amount']) + list(self.sponsors['amount'])
        return pd.DataFrame(list(zip(ids, amount)), columns=['transaction_id', 'amount'])

if __name__ == "__main__":
    print("Script running...")
    # Create sqlalchemy engine
    engine = create_engine('mysql+pymysql://team7:%s@giniewicz.it:3306/team7' % quote('te@mTP@ss'))

    # Generate tables

    db_p = DbFiller("player", 500)
    players = db_p.generate()
    players.to_sql('player', con = engine, if_exists = 'replace', index = False)

    db_sp = DbFiller("sponsors", 500)
    sponsors = db_sp.generate()
    sponsors.to_sql('sponsor', con = engine, if_exists = 'replace', index = False)

    db_st = DbFiller("staff", 81)
    staff = db_st.generate()
    staff.to_sql('staff', con = engine, if_exists = 'replace', index = False)

    db_e = DbFiller("equipment", 500)
    equipment = db_e.generate()
    equipment.to_sql('equipment', con = engine, if_exists = 'replace', index = False)

    # Male teams = id + 10000; Female teams = id + 20000
    db2 = DbFiller2(players)
    teams = db2.generate()
    teams.to_sql('team', con = engine, if_exists = 'replace', index = False)

    db3 = DbFiller3(teams)
    matches, scores = db3.generate(staff)
    matches.to_sql('match', con = engine, if_exists = 'replace', index = False)
    scores.to_sql('scores', con = engine, if_exists = 'replace', index = False)

    db4 = DbFiller4(sponsors, staff, equipment)
    expenses = db4.transaction_eq()
    salaries = db4.generate_salaries()
    spons_trans = db4.sponsors_transactions()

    expenses.to_sql('expenses', con = engine, if_exists = 'replace', index = False)
    salaries.to_sql('salary', con = engine, if_exists = 'replace', index = False)
    spons_trans.to_sql('sponsor_transaction', con = engine, if_exists = 'replace', index = False)


    db5 = DbFiller5(salaries, expenses, spons_trans)
    financial = db5.financials()
    financial.to_sql('financials', con = engine, if_exists = 'replace', index = False)


