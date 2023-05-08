import pandas as pd


def fit_op_divide(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    denom = df2.reindex(index=df1.index, columns=df1.columns)
    return df1.divide(denom, axis=1)


def candle_sim(
    simpos_df: pd.DataFrame,
    fill_price_df: pd.DataFrame,
    ref_price_df: pd.DataFrame = None,
    fee: float or int = None,
) -> pd.DataFrame:
    """
    Assume: 
    - open convention: simpos_df
    - close convention: prices
    """
    value_df = simpos_df.shift(1).fillna(0.0) # close convention

    if ref_price_df is None:
        ref_price_df = fill_price_df
    count_df = fit_op_divide(value_df, ref_price_df)
    dcount_df = count_df.fillna(0.0).diff()

    holding = value_df.diff()
    trading = -dcount_df * fill_price_df
    simpnl_df = holding + trading

    if fee:
        simpnl_df -= (trading * fee).abs()

    return simpnl_df
