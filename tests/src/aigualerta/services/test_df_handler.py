import unittest
from unittest import mock
import numpy as np
import pandas as pd
import aigualerta.constants as constants

from aigualerta.services import df_handler

class TestDfHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Sample DataFrame with original column names and datetime including hour
        cls.df_original = pd.DataFrame({
            'Pòlissa/Póliza/Policy': ['policy1', 'policy1', 'policy2', 'policy2'],
            'Data/Fecha/Date': ['2023-01-01 10:00:00', '2023-01-02 11:00:00', '2023-01-03 12:00:00', '2023-01-04 13:00:00'],
            'Índex de lectura (L/h)/Índice de lectura (L/h)/Reading index (L/h)': [10, 12, 15, 13],
            'Tecnologia/Tecnología/Technology': ['tech1', 'tech1', 'tech2', 'tech2'],
            'Diàmetre comptador (cm)/Diámetro contador (cm)/Counter diameter (cm)': [20, 20, 25, 25],
            'Ús/Uso/Use': ['use1', 'use1', 'use2', 'use2'],
            "Tipus d'habitatge/Tipo de vivienda/Type of housing": ['housing1', 'housing1', 'housing2', 'housing2']
        })

        cls.df_not_missing_column = pd.DataFrame({
            'POLICY': ['policy1', 'policy1', 'policy2', 'policy2'],
            'DATETIME': ['2023-01-01 10:00:00', '2023-01-02 11:00:00', '2023-01-03 12:00:00', '2023-01-04 13:00:00'],
            'CONSUMPTION': [10, 12, 15, 13],
            'TECHNOLOGY': ['tech1', 'tech1', 'tech2', 'tech2'],
            'DIAMETER': [20, 20, 25, 25],
            'USAGE': ['use1', 'use1', 'use2', 'use2'],
            'HOUSING': ['housing1', 'housing1', 'housing2', 'housing2']
        })

        cls.expected_df = pd.DataFrame({
                'POLICY': ['policy1', 'policy2'],
                'DATETIME': pd.to_datetime(['2023-01-02 11:00:00', '2023-01-04 13:00:00']),
                'CONSUMPTION': [12, 13],
                'TECHNOLOGY': ['tech1', 'tech2'],
                'DIAMETER': [20, 25],
                'USAGE': ['use1', 'use2'],
                'HOUSING': ['housing1', 'housing2'],
                'WEEKDAY': pd.Series([0, 2], dtype='int32'),
                'HOUR': pd.Series([11, 13], dtype='int32'),
                'FLOW': [2.0, -2.0]
            })

    def setUp(self):
        # Reset mocks before each test
        mock.patch('pickle.load').start()
        mock.patch('pandas.to_datetime').start()

    def tearDown(self):
        # Stop mocks after each test
        mock.patch('pickle.load').stop()
        mock.patch('pandas.to_datetime').stop()

    def testRenameColumns(self):
        new_df = df_handler.rename_columns(self.df_original.copy())
        self.assertEqual(list(new_df.columns).sort(), list(constants.EXPECTED_COLUMNS).sort())

    def testMissingColumnsReturnsTrue(self):
        df_missing_column = pd.DataFrame({
            'POLICY': ['policy1', 'policy1', 'policy2', 'policy2'],
            'CONSUMPTION': [10, 12, 15, 13],
            'TECHNOLOGY': ['tech1', 'tech1', 'tech2', 'tech2'],
            'DIAMETER': [20, 20, 25, 25],
            'USAGE': ['use1', 'use1', 'use2', 'use2'],
            'HOUSING': ['housing1', 'housing1', 'housing2', 'housing2']
        })
        self.assertTrue(df_handler.is_missing_columns(df_missing_column))

    def testMissingColumnsReturnsFalse(self):
        self.assertFalse(df_handler.is_missing_columns(self.df_not_missing_column))

    def testTransformColumns(self):
        with mock.patch('pandas.to_datetime', new=pd.core.tools.datetimes.to_datetime):
            input_df = pd.DataFrame({
                'POLICY': ['policy1', 'policy1', 'policy2', 'policy2'],
                'DATETIME': ['2023-01-01 10:00:00', '2023-01-02 11:00:00', '2023-01-03 12:00:00', '2023-01-04 13:00:00'],
                'CONSUMPTION': [10, 12, 15, 13],
                'TECHNOLOGY': ['tech1', 'tech1', 'tech2', 'tech2'],
                'DIAMETER': [20, 20, 25, 25],
                'USAGE': ['use1', 'use1', 'use2', 'use2'],
                'HOUSING': ['housing1', 'housing1', 'housing2', 'housing2']
            })
            
            transformed_df = df_handler.transform_columns(input_df.copy())

            # Reset the index of the transformed DataFrame
            transformed_df.reset_index(drop=True, inplace=True)

            # Assert that the transformed DataFrame matches the expected DataFrame
            pd.testing.assert_frame_equal(transformed_df, self.expected_df)

    def testDropDefectiveRows(self):
        with mock.patch('pandas.to_datetime', new=pd.core.tools.datetimes.to_datetime):
            input_df = pd.DataFrame({
                'POLICY': ['policy1', 'policy1', 'policy2', 'policy2', 'policy3', 'policy3'],
                'DATETIME': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06']),
                'CONSUMPTION': [10, 12, 15, 13, 18, 16],
                'TECHNOLOGY': ['tech1', 'tech1', 'tech2', 'tech2', 'tech1', 'tech1'],
                'DIAMETER': [20, 20, 25, 25, 20, 20],
                'USAGE': ['use1', 'use1', 'use2', 'use2', 'use1', 'use1'],
                'HOUSING': ['housing1', 'housing1', 'housing2', 'housing2', 'housing1', 'housing1'],
                'FLOW': [np.nan, 2.0, np.nan, -2.0, np.nan, -2.0]
            })

            # Expected output DataFrame after removing defective rows
            expected_df = pd.DataFrame({
                'POLICY': ['policy1'],
                'DATETIME': pd.to_datetime(['2023-01-02']),
                'CONSUMPTION': [12],
                'TECHNOLOGY': ['tech1'],
                'DIAMETER': [20],
                'USAGE': ['use1'],
                'HOUSING': ['housing1'],
                'FLOW': [2.0]
            })

            # Apply the function
            transformed_df = df_handler.drop_defective_rows(input_df.copy())

            # Assert that the transformed DataFrame matches the expected DataFrame
            pd.testing.assert_frame_equal(transformed_df.reset_index(drop=True), expected_df)

    @mock.patch('aigualerta.services.df_handler.drop_defective_rows')
    @mock.patch('aigualerta.services.df_handler.transform_columns')
    @mock.patch('aigualerta.services.df_handler.is_missing_columns')
    @mock.patch('aigualerta.services.df_handler.rename_columns')
    def testPrepareDataNoMissingColumns(self, rename_mock, missing_mock, transform_mock, drop_mock):
        # Mock the return values of the functions
        rename_mock.return_value = "renamed_df"
        missing_mock.return_value = False
        transform_mock.return_value = "transformed_df"
        drop_mock.return_value = "final_df"

        result_df = df_handler.prepare_data("some_mock")

        rename_mock.assert_called_with("some_mock")
        missing_mock.assert_called_once()
        transform_mock.assert_called_with("renamed_df")
        drop_mock.assert_called_with("transformed_df")
        self.assertEqual(result_df, "final_df")
        
    @mock.patch('aigualerta.services.df_handler.is_missing_columns')
    @mock.patch('aigualerta.services.df_handler.rename_columns')
    def testPrepareDataMissingColumns(self, rename_mock, missing_mock):
        rename_mock.return_value = "renamed_df"
        missing_mock.return_value = True

        result_df = df_handler.prepare_data("some_mock")

        rename_mock.assert_called_with("some_mock")
        self.assertEqual(result_df, None)

    def test_setup_input(self):
        with mock.patch('pandas.to_datetime', new=pd.core.tools.datetimes.to_datetime):
            # Input DataFrame
            input_df = pd.DataFrame({
                'POLICY': ['policy1', 'policy1', 'policy1', 'policy1', 'policy1'],
                'DATETIME': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']),
                'CONSUMPTION': [10, 12, 14, 16, 18],
                'TECHNOLOGY': ['tech1', 'tech1', 'tech1', 'tech1', 'tech1'],
                'DIAMETER': [20, 20, 20, 20, 20],
                'USAGE': ['use1', 'use1', 'use1', 'use1', 'use1'],
                'HOUSING': ['housing1', 'housing1', 'housing1', 'housing1', 'housing1'],
                'FLOW': [1.0, 2.0, 2.0, 2.0, 2.0],
                'WEEKDAY': [6, 0, 1, 2, 3],
                'HOUR': [10, 11, 12, 13, 14]
            })

            # Expected output DataFrame (with window_size = 4)
            expected_df = pd.DataFrame({
                'POLICY': ['policy1', 'policy1'],
                'TECHNOLOGY': ['tech1', 'tech1'],
                'USAGE': ['use1', 'use1'],
                'HOUSING': ['housing1', 'housing1'],
                'CONSUMPTION': [10, 12],
                'DATETIME': pd.to_datetime(['2023-01-01', '2023-01-02']),
                'WEEKDAY': [6, 0],
                'START_HOUR': [10, 11],
                'FLOW_1': [1.0, 2.0],
                'FLOW_2': [2.0, 2.0],
                'FLOW_3': [2.0, 2.0],
                'FLOW_4': [2.0, 2.0],
            })

        # Apply the function with window_size = 4
        transformed_df = df_handler.setup_input(input_df.copy(), window_size=4)
        print(transformed_df)

        # Assert that the transformed DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(transformed_df.reset_index(drop=True), expected_df)

    def test_predict(self):
        with mock.patch('pandas.to_datetime', new=pd.core.tools.datetimes.to_datetime):
            input_df = pd.DataFrame({
                'POLICY': ['policy1', 'policy2'],
                'TECHNOLOGY': ['tech1', 'tech2'],
                'USAGE': ['use1', 'use2'],
                'HOUSING': ['housing1', 'housing2'],
                'CONSUMPTION': [10, 12],
                'DATETIME': pd.to_datetime(['2023-01-01', '2023-01-02']),
                'WEEKDAY': [6, 0],
                'START_HOUR': [10, 11],
                'FLOW_1': [1.0, 2.0],
                'FLOW_2': [2.0, 3.0],
                'FLOW_3': [3.0, 4.0],
                'FLOW_4': [4.0, 5.0],
            })

        transformed_df = df_handler.predict(input_df.copy())

        # Expected output DataFrame
        expected_df = input_df.copy()
        expected_df['LEAK'] = [False, False]

        # Assert that the transformed DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(transformed_df, expected_df)

    @mock.patch('aigualerta.services.df_handler.prepare_data')
    @mock.patch('aigualerta.services.df_handler.setup_input')
    @mock.patch('aigualerta.services.df_handler.predict')
    @mock.patch('streamlit.session_state')
    @mock.patch('streamlit.balloons')
    def test_compute_results(self, mock_balloons, mock_session_state, mock_predict, mock_setup_input, mock_prepare_data):
        mock_loading_bar = mock.MagicMock()

        mock_prepare_data.return_value = "prepared_df"
        mock_setup_input.return_value = "input_df"
        mock_predict.return_value = "predicted_df"

        result_df = df_handler.compute_results("original_df", mock_loading_bar)

        mock_prepare_data.assert_called_once_with("original_df")
        mock_setup_input.assert_called_once_with("prepared_df")
        mock_predict.assert_called_once_with("input_df")

        self.assertEqual(mock_session_state.setup_df, "prepared_df")
        self.assertEqual(mock_session_state.input_df, "input_df")
        self.assertEqual(mock_session_state.predicted_df, "predicted_df")

        mock_loading_bar.progress.assert_has_calls([
            mock.call(34, text="Setting up"),
            mock.call(66, text="Predicting"),
            mock.call(100, text="Done!"),
        ])
        
        mock_balloons.assert_called_once()

        # Assert the return value
        self.assertEqual(result_df, "predicted_df")