def get_lot(ids, contact_info, document, price, trade, info):
    lot = {
        "tradeLotId": ids["trade_lot"],
        "applicationId": ids["application"],
        "contactPerson": contact_info["person"],
        "contactData": contact_info["data"],
        "isAgreeToSupply": True,
        "deliveryPrice": 0,
        "documents": [document],
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

    # {
    #     "tradeLotId": "7b5bc423-55a3-4121-abd6-4ecb58c230fb",
    #     "applicationId": "c1a39240-fb19-4951-b04b-c80c9d98c710",
    #     "contactPerson": "Кузнецова  Ксения Геннадиевна",
    #     "contactData": "тел. +7(989)621-05-03, sperik_ice@mail.ru",
    #     "isAgreeToSupply": true,
    #     "deliveryPrice": 0,
    #     "documents": [],
    #     "items": [
    #         {
    #             "quotation": 2346.6,
    #             "quantity": 1,
    #             "tradeLotItemOrder": 0,
    #             "taxPercent": null,
    #             "name": "Услуги по обязательному страхованию гражданской ответственности владельца транспортных средств",
    #             "offerId": "00000000-0000-0000-0000-000000000000",
    #             "offerNumber": null,
    #             "countryOfOrigin": null,
    #             "isPriceWithTax": true,
    #             "calculatedTax": 0,
    #             "sum": 2346.6,
    #             "offerName": null,
    #             "description": "Марка, модель ТС : ГАЗ-3221\nИдентификационный номер (VIN): ХТН32210030333979\nГод ВЫПУСКА: 2003\nМощность двигателя, КВт/л.с.: 72,2\nПаспорт ТС 52КР752156 от 18.09.2003\nг.р.н. О846РВ74\nРазрешенная максимальная масса, кг 3250\nШасси -\nКузов (прицеп) 32210030058531",
    #             "offerDescription": null,
    #             "priceOption": 1,
    #             "requireOfferSpecification": false,
    #             "russianItemsRegistryNum": null,
    #             "russianItemsRegistry": null,
    #             "isSelected": false,
    #             "referenceOfferId": null,
    #             "referenceOfferNumber": null,
    #             "isReference": false
    #         }
    #     ],
    #     "applicationSubType": 0,
    #     "applicationPriceHidden": false,
    #     "sessionConclusionContractPrice": null,
    #     "decreasePercent": null,
    #     "unitPriceSum": 2346.6,
    #     "calculatedTax": 0,
    #     "taxPercent": 0
    # }