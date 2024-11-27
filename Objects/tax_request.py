def get_tax(unit_price):
    task = {
        "amount": 1,
        "isPriceWithTax": True,
        "quantityUndefined": False,
        "tax": 1000,
        "unitPrice": unit_price
    }

    return task
