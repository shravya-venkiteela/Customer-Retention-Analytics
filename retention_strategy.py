def retention_action(segment):

    if segment == "Champions":
        return "VIP Rewards Program"

    elif segment == "Loyal Customers":
        return "Upsell Premium Products"

    elif segment == "Potential Loyalists":
        return "Personalized Email Campaign"

    elif segment == "At Risk":
        return "Discount Retention Campaign"

    elif segment == "Lost Customers":
        return "Win-Back Offer"

    else:
        return "No Action"