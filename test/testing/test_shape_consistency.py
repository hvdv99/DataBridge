import pytest
from test.testing.functions import answer, answer_vanna

# This function should be filled dynamically, so leave it as a placeholder.
prepared_data = []

@pytest.mark.parametrize("category,number,question,expected_sql,experimental_sql", prepared_data)
def test_sql_query_shape_consistency(category, number, question, expected_sql, experimental_sql):
    """
    Test to ensure that SQL queries produce dataframes of the same shape.
    This validates that the structure (number of rows and columns) is consistent between the two dataframes.
    """
    df_expected = answer(expected_sql)
    df_experimental = answer_vanna(experimental_sql)
    assert df_expected.shape == df_experimental.shape, \
        f"DataFrames do not have the same shape: {df_expected.shape} != {df_experimental.shape}\
        \nFor question: {question}"
