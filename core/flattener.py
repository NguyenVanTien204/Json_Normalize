def flatten_dict(obj, sep=".", explode_arrays=False, flatten_nested=False):
    """
    Flatten a nested dictionary into a flat dictionary or list of dictionaries if exploding arrays.

    Args:
        obj (dict): The nested dictionary to flatten.
        sep (str): The separator for flattened keys. Default is ".".
        explode_arrays (bool): If True, explode primitive arrays into multiple rows. Default is False.
        flatten_nested (bool): If True, flatten nested arrays. Default is False.

    Returns:
        list[dict]: List of flattened dictionaries.
    """
    def _flatten(current, prefix="", path=[]):
        results = []
        if isinstance(current, dict):
            for key, value in current.items():
                new_prefix = f"{prefix}{sep}{key}" if prefix else key
                new_path = path + [key]
                sub_results = _flatten(value, new_prefix, new_path)
                if not results:
                    results = sub_results
                else:
                    # Combine with existing results
                    new_results = []
                    for res in results:
                        for sub_res in sub_results:
                            combined = res.copy()
                            combined.update(sub_res)
                            new_results.append(combined)
                    results = new_results
        elif isinstance(current, list):
            if flatten_nested and any(isinstance(item, list) for item in current):
                # Flatten nested arrays
                flat_list = []
                for item in current:
                    if isinstance(item, list):
                        flat_list.extend(item)
                    else:
                        flat_list.append(item)
                current = flat_list

            if explode_arrays and all(not isinstance(item, (dict, list)) for item in current):
                # Primitive array, explode
                for item in current:
                    results.append({prefix: item})
            else:
                # Keep as is
                results.append({prefix: current})
        else:
            results.append({prefix: current})

        if not results:
            results = [{}]
        return results

    return _flatten(obj)
