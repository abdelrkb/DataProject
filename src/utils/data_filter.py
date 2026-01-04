def filter_by_geo(df, region=None, dep=None):
    """
    Filtre un DataFrame par région ou département.

    Args:
        df (pandas.DataFrame): DataFrame contenant les données.
        region (str | None): Nom de la région à filtrer.
        dep (str | None): Nom du département à filtrer.

    Returns:
        pandas.DataFrame: Vue filtrée sur Région ou département.
    """
    if dep:
        return df[df["lib_dep"] == dep]

    if region:
        return df[df["lib_reg"] == region]

    return df


def available_regions(df):
    """
    Retourne la liste triée des régions présentes dans le DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame.

    Returns:
        list[str]: Liste triée des noms de régions.
    """
    values = df["lib_reg"].dropna().unique().tolist()

    return sorted(values)


def available_dep(df):
    """
    Retourne la liste triée des départements présents dans le DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame.

    Returns:
        list[str]: Liste triée des noms de départements.
    """
    values = df["lib_dep"].dropna().unique().tolist()

    return sorted(values)
