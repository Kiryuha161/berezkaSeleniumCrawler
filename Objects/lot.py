def get_lot(ids, contact_info, document, price, trade, info):
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
        "items": [
            {
                "quotation": price,
                "quantity": info["items"][0]["calculatedTax"],
                "tradeLotItemOrder": 0,
                "taxPercent": 0,  # 0 или 1000?
                "name": info["items"][0]["name"],
                "offerId": info["items"][0]["offerId"],
                "offerNumber": info["items"][0]["offerNumber"],
                "countryOfOrigin": info["items"][0]["countryOfOrigin"],
                "isPriceWithTax": info["items"][0]["isPriceWithTax"],
                "calculatedTax": info["items"][0]["calculatedTax"],
                "sum": info["items"][0]["sum"],
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
            }
        ],
        "applicationSubType": info["applicationSubType"],
        "applicationPriceHidden": False,
        "sessionConclusionContractPrice": info["sessionConclusionContractPrice"],
        "decreasePercent": None,
        "unitPriceSum": price,
        "calculatedTax": 0,  # 0 или 1000?
        "taxPercent": 0  # 0 или 1000?
    }

    return lot

    # lot = {
    #     "tradeLotId": "f34b0b6c-3e7f-4b4e-9136-a8c9293535c4",
    #     "applicationId": "9d56d22c-1a23-4f9b-af70-569c091f786b",
    #     "contactPerson": "Кузнецова  Ксения Геннадиевна",
    #     "contactData": "тел. +7(989)621-05-03, sperik_ice@mail.ru",
    #     "isAgreeToSupply": True,
    #     "deliveryPrice": 0,
    #     "documents": [
    #         {
    #             "id": "a87c577c-97bf-4735-82ba-e890663c5d0e",
    #             "type": 0,
    #             "size": 6356006,
    #             "name": "Заявки Транстех Березка.zip",
    #             "version": None,
    #             "isActual": None,
    #             "typeName": None,
    #             "documentName": None,
    #             "createdOn": "2024-12-09T07:11:12Z",
    #             "sendDate": None
    #         }
    #     ],
    #     "items": [
    #         {
    #             "quotation": 7000,
    #             "quantity": 1,
    #             "tradeLotItemOrder": 0,
    #             "taxPercent": None,
    #             "name": None,
    #             "offerId": "00000000-0000-0000-0000-000000000000",
    #             "offerNumber": None,
    #             "countryOfOrigin": None,
    #             "isPriceWithTax": True,
    #             "calculatedTax": 0,
    #             "sum": 7000,
    #             "offerName": None,
    #             "description": "Поставка товара согласно спецификации, без аналогов и замен.",
    #             "offerDescription": None,
    #             "priceOption": 1,
    #             "requireOfferSpecification": False,
    #             "russianItemsRegistryNum": None,
    #             "russianItemsRegistry": None,
    #             "isSelected": False,
    #             "referenceOfferId": None,
    #             "referenceOfferNumber": None,
    #             "isReference": False
    #         }
    #     ],
    #     "applicationSubType": 0,
    #     "applicationPriceHidden": False,
    #     "sessionConclusionContractPrice": None,
    #     "decreasePercent": None,
    #     "unitPriceSum": 0,
    #     "calculatedTax": 0,
    #     "taxPercent": 0
    # }