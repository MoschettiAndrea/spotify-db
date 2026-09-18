import pandas as pd

def reconcile(new_df, existing_df, key_cols, id_col):
    """
    Compare freshly parsed rows against what's already in the DB, matched
    on key_cols (never id_col). Returns:
      - id_map: key_cols -> id, covering BOTH existing and newly assigned ids
      - to_insert: only the rows that don't already exist, with id_col
        continuing on from the existing table's max id
    """
    for col in key_cols:
        if new_df[col].dtype != existing_df[col].dtype:
            raise TypeError(
                f"dtype mismatch on '{col}': new={new_df[col].dtype}, "
                f"existing={existing_df[col].dtype} — dedup will silently fail"
            )

    existing_keyed = existing_df.set_index(key_cols)
    start_id = int(existing_df[id_col].max()) + 1 if not existing_df.empty else 1

    new_keyed = new_df.set_index(key_cols)
    is_new = ~new_keyed.index.isin(existing_keyed.index)

    to_insert = new_keyed[is_new].reset_index()
    to_insert[id_col] = range(start_id, start_id + len(to_insert))

    id_map = pd.concat([existing_keyed[id_col], to_insert.set_index(key_cols)[id_col]])

    cols = [id_col] + [c for c in new_df.columns if c != id_col]
    return id_map, to_insert[cols]