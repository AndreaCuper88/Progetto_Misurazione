CASES = {
    1: {
        "nome": "Assoluto - WCU",
        "tipo_input": "abs_wcu", #incertezze assolute di caso peggiore
        "tipo_propagazione": "wcu",
        "domande": [
            "cx1",
            "cx2",
            "Ux",
            "Urx",
            "ux",
            "crphi"
        ]
    },

    2: {
        "nome": "Assoluto - Standard",
        "tipo_input": "abs_std",    #incertezze assolute standard
        "tipo_propagazione": "std",
        "domande": [
            "cx1",
            "cx2",
            "Ux",
            "Urx",
            "ux",
            "crphi"
        ]
    },

    3: {
        "nome": "Relativo - WCU",
        "tipo_input": "rel_wcu",    #incertezze relative di caso peggiore
        "tipo_propagazione": "wcu",
        "domande": [
            "crx1",
            "crx2",
            "Urx",
            "Ux",
            "urx",
            "cphi"
        ]
    },

    4: {
        "nome": "Relativo - Standard",
        "tipo_input": "rel_std",    #incertezze relative standard
        "tipo_propagazione": "std",
        "domande": [
            "crx1",
            "crx2",
            "Urx",
            "Ux",
            "urx",
            "cphi"
        ]
    }
}