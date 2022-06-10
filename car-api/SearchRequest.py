# This was horrible to write...
class SearchRequest:
    def ParsePair(obj, start, end, base):
        if type(obj[start]) is not int:
            if obj[start].isdigit():
                start = int(obj[start])
            else:
                return ""
        else:
            start = obj[start]

        if type(obj[end]) is not int:
            if obj[end].isdigit():
                end = int(obj[end])
            else:
                return ""
        else:
            end = obj[end]

        if start > 0 and end > 0:
            return f" {base} >= {start} AND {base} =< {end} AND"
        else:
            return ""
    
    def GetQuerry(obj):
        querry = "SELECT * FROM cars WHERE"

        if type(obj["model"]) is not int:
            if obj["model"].isdigit():
                model = int(obj["model"])
        else:
            model = obj["model"]

        if model > 0:
            querry += f" model = {model} AND"

        querry += SearchRequest.ParsePair(obj, "year_start", "year_end", "year")
        querry += SearchRequest.ParsePair(obj, "km_start", "km_end", "km")
        querry += SearchRequest.ParsePair(obj, "price_start", "price_end", "price")
        querry += SearchRequest.ParsePair(obj, "bhp_start", "bhp_end", "bhp")

        # Remove the trailing "and"
        querry = " ".join(str(x) for x in querry.split(" ")[:-1])
        return querry


    """
    model,
    year range,
    km range,
    price ranga,
    bhp range
    """