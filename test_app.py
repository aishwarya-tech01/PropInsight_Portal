import unittest
import sqlite3
import pandas as pd

class TestPropInsightDataEngine(unittest.TestCase):

    def setUp(self):
        """
        Runs automatically before each test scenario.
        Sets up an isolated, pure in-memory test database structure.
        """
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        
        # Build an exact twin mirror replica of our master production database listings table
        self.cursor.execute('''
            CREATE TABLE listings (
                property_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT, locality TEXT, bedrooms INTEGER, price REAL, square_feet INTEGER
            )
        ''')
        
        # Inject carefully weighted test listings to evaluate mathematical equations
        self.sample_data = [
            ('Standard Test Flat', 'Kothrud', 2, 6000000, 1000),      # Rate = 6000/sqft
            ('Bargain Asset Test Flat', 'Kothrud', 2, 4000000, 1000), # Rate = 4000/sqft (Lower than avg!)
            ('Luxury Test Villa', 'Kothrud', 3, 8000000, 1000)        # Rate = 8000/sqft
        ]
        self.cursor.executemany(
            "INSERT INTO listings (title, locality, bedrooms, price, square_feet) VALUES (?, ?, ?, ?, ?)", 
            self.sample_data
        )
        self.conn.commit()

    def tearDown(self):
        """
        Runs automatically after each test scenario to leave a clean environment space.
        """
        self.conn.close()

    def test_cost_per_sqft_calculation(self):
        """
        🧪 TEST SCENARIO 1: Verifies that the engine handles relational 
        division math equations with perfect precision.
        """
        query = "SELECT *, (price / square_feet) AS cost_per_sqft FROM listings WHERE title = ?"
        df = pd.read_sql_query(query, self.conn, params=['Standard Test Flat'])
        
        calculated_rate = df.iloc[0]['cost_per_sqft']
        expected_rate = 6000000 / 1000  # 6000
        
        # Programmatic Assertion Check
        self.assertEqual(calculated_rate, expected_rate, "❌ Mathematics Error: Price per sqft calculation mismatch!")

    def test_automated_bargain_detection_logic(self):
        """
        🧪 TEST SCENARIO 2: Verifies that the algorithmic bargain marker engine
        correctly isolates properties sitting below baseline neighborhood averages.
        """
        # Fetch matching rows matching baseline matrix routines
        df_properties = pd.read_sql_query("SELECT *, (price / square_feet) AS cost_per_sqft FROM listings", self.conn)
        
        # Calculate baseline neighborhood average matching main application primitives
        baseline_avg = df_properties['cost_per_sqft'].mean() # (6000 + 4000 + 8000) / 3 = 6000
        
        # Isolate the targeted bargain rows match target
        bargain_row = df_properties[df_properties['title'] == 'Bargain Asset Test Flat'].iloc[0]
        standard_row = df_properties[df_properties['title'] == 'Luxury Test Villa'].iloc[0]
        
        # Assertions: Bargain asset rate (4000) must be lower than baseline average (6000)
        self.assertTrue(bargain_row['cost_per_sqft'] < baseline_avg, "❌ Bargain asset failure!")
        self.assertFalse(standard_row['cost_per_sqft'] < baseline_avg, "❌ Standard asset flagged as bargain erroneously!")

if __name__ == '__main__':
    unittest.main()