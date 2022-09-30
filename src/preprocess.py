import polars as pl


def prepare_floats(filename, modelsettings) -> pl.DataFrame:
    target = modelsettings.target

    df = pl.read_parquet(filename)
    p = (
        df.select(
            [
                pl.col(pl.Float64),  # select float
                pl.col(target),  # and the target column
            ]
        )
        .melt(id_vars=target)
        .select(
            [  # melt on target
                pl.col("*"),
                pl.col("value")
                .mean()
                .over("variable")
                .alias("mean/var"),  # create mean
                pl.col("value").std().over("variable").alias("std/var"),  # and std
            ]
        )
        .with_columns(
            [
                pl.struct(["value", "mean/var", "std/var"])
                .apply(lambda x: (x["value"] - x["mean/var"]) / x["std/var"])
                .alias("norm")
            ]
        )
    )  # to normalize the data

    return p
