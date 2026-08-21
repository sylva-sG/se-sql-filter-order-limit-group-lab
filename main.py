import pandas as pd
import sqlite3

##### Part I: Basic Filtering #####

# Create the connection
conn1 = sqlite3.connect('planets.db')

# Select all base dataframe structure
planets_raw = pd.read_sql("""SELECT * FROM planets; """, conn1)

# STEP 1
# Return all columns for planets that have 0 moons, matching dynamically via schema checks
moon_col = [col for col in planets_raw.columns if 'moon' in col.lower()]
df_no_moons = planets_raw[planets_raw[moon_col[0]] == 0].reset_index(drop=True)

# STEP 2
# Return the name and mass of each planet that has a name with exactly 7 letters
df_name_seven = pd.read_sql(
    """
    SELECT name, mass 
    FROM planets 
    WHERE LENGTH(name) = 7;
    """, 
    conn1
)

##### Part 2: Advanced Filtering #####

# STEP 3
# Return name and mass for each planet with a mass less than or equal to 1.00
df_mass = pd.read_sql(
    """
    SELECT name, mass 
    FROM planets 
    WHERE mass <= 1.00;
    """, 
    conn1
)

# STEP 4
# Return all columns for planets that have at least one moon and a mass less than 1.00
df_mass_moon = planets_raw[(planets_raw[moon_col[0]] >= 1) & (planets_raw['mass'] < 1.00)].reset_index(drop=True)

# STEP 5
# Return name and color of planets with a color containing the string "blue"
df_blue = pd.read_sql(
    """
    SELECT name, color 
    FROM planets 
    WHERE color LIKE '%blue%';
    """, 
    conn1
)

##### Part 3: Ordering and Limiting #####

# STEP 0
conn2 = sqlite3.connect('dogs.db')
pd.read_sql("SELECT * FROM dogs;", conn2)

# STEP 6
# Return name, age, and breed of hungry dogs, sorted from youngest to oldest
df_hungry = pd.read_sql(
    """
    SELECT name, age, breed 
    FROM dogs 
    WHERE hungry = 1
    ORDER BY age ASC;
    """, 
    conn2
)


# STEP 7
# Hungry dogs between ages 2 and 7. Sorted alphabetically by name.
df_hungry_ages = pd.read_sql(
    """
    SELECT name, age, hungry 
    FROM dogs 
    WHERE hungry = 1 AND age BETWEEN 2 AND 7
    ORDER BY name ASC;
    """, 
    conn2
)

#  STEP 8
# Return name, age, breed for the 4 oldest dogs, sorted alphabetically by breed, 
# and reverse alphabetically by name to break ties for identical breeds.
df_4_oldest = pd.read_sql(
    """
    SELECT name, age, breed
    FROM dogs
    ORDER BY age DESC
    LIMIT 4;
    """,
    conn2
)


##### Part 4: Aggregation #####

# STEP 0
conn3 = sqlite3.connect('babe_ruth.db')
pd.read_sql("""SELECT * FROM babe_ruth_stats; """, conn3)

# STEP 9
# Total number of years Babe Ruth played professional baseball
df_ruth_years = pd.read_sql(
    """
    SELECT COUNT(year) 
    FROM babe_ruth_stats;
    """, 
    conn3
)

# STEP 10
# Total number of home runs hit by Babe Ruth during his career
df_hr_total = pd.read_sql(
    """
    SELECT SUM(hr) 
    FROM babe_ruth_stats;
    """, 
    conn3
)


##### Part 5: Grouping and Aggregation #####

# STEP 11
# Return team name and the number of years he played on that team, aliased as number_years
df_teams_years = pd.read_sql(
    """
    SELECT team, COUNT(year) AS number_years 
    FROM babe_ruth_stats 
    GROUP BY team;
    """, 
    conn3
)

# STEP 12
# For teams averaging > 200 at-bats, return team name and average at-bats, aliased as average_at_bats
df_at_bats = pd.read_sql(
    """
    SELECT team, AVG(at_bats) AS average_at_bats 
    FROM babe_ruth_stats 
    GROUP BY team 
    HAVING AVG(at_bats) > 200;
    """, 
    conn3
)

conn1.close()
conn2.close()
conn3.close()
