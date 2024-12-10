def get_lot(ids, contact_info, document, price, trade, info):
    print(f"Внутри get_lot: {ids["trade_lot"]=}")
    lot = {
        "tradeLotId": ids["trade_lot"],
        "applicationId": ids["application"],
        "contactPerson": contact_info["person"],
        "contactData": contact_info["data"],
        "isAgreeToSupply": True,
        "deliveryPrice": 0,
        "documents": [
            document
        ],
        "items": [],
        "applicationSubType": info["applicationSubType"],
        "applicationPriceHidden": False,
        "sessionConclusionContractPrice": info["sessionConclusionContractPrice"],
        "decreasePercent": None,
        "unitPriceSum": price,
        "calculatedTax": 0,  # 0 или 1000?
        "taxPercent": 0  # 0 или 1000?
    }

    for item in info["items"]:
        item_sum = item["quantity"] * price
        lot["items"].append({
            "quotation": price,
            "quantity": item["quantity"],
            "tradeLotItemOrder": 0,
            "taxPercent": 0,  # 0 или 1000?
            "name": item["name"],
            "offerId": item["offerId"],
            "offerNumber": item["offerNumber"],
            "countryOfOrigin": item["countryOfOrigin"],
            "isPriceWithTax": item["isPriceWithTax"],
            "calculatedTax": 0,
            "sum": item_sum,
            "offerName": None,
            "description": trade["lot"]["lotItems"][0]["description"],
            "offerDescription": None,
            "priceOption": trade["lot"]["lotItems"][0]["priceOption"],
            "requireOfferSpecification": trade["lot"]["lotItems"][0]["requireOfferSpecification"],
            "russianItemsRegistryNum": trade["lot"]["lotItems"][0]["russianItemsRegistryNum"],
            "russianItemsRegistry": trade["lot"]["lotItems"][0]["russianItemsRegistry"],
            "isSelected": False,
            "referenceOfferId": trade["lot"]["lotItems"][0]["referenceOfferId"],
            "referenceOfferNumber": trade["lot"]["lotItems"][0]["referenceOfferNumber"],
            "isReference": trade["lot"]["lotItems"][0]["isReference"]
        })

    return lot
