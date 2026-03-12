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
        ],
        "soluzione": {
            "Ux": {
                "msg": "% Incertezza di caso peggiore assoluta",
                "formula": "abs(cx1)*Ux1 + abs(cx2)*Ux2 + abs(cphi)*Uphi"
            },
            "Urx": {
                "msg": "% Incertezza di caso peggiore relativa",
                "formula": "Ux/abs(x)"
            },
            "ux": {
                "msg": "% Incertezza standard assoluta",
                "formula": "Ux/sqrt(3)"
            }
        }
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
        ],
        "soluzione": {
            "ux": {
                "msg": "% Incertezza standard assoluta",
                "formula": "sqrt((cx1*ux1)^2 + (cx2*ux2)^2 + (cphi*uphi)^2)"
            },
            "Ux": {
                "msg": "% Incertezza di caso peggiore assoluta",
                "formula": "sqrt(3)*ux"
            },
            "Urx": {
                "msg": "% Incertezza di caso peggiore relativa",
                "formula": "Ux/abs(x)"
            }
        }
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
        ],
        "soluzione": {
            "Urx": {
                "msg": "% Incertezza di caso peggiore relativa",
                "formula": "abs(crx1)*Urx1 + abs(crx2)*Urx2 + abs(crphi)*Urphi"
            },
            "Ux": {
                "msg": "% Incertezza di caso peggiore assoluta",
                "formula": "Urx*abs(x)"
            },
            "urx": {
                "msg": "% Incertezza standard relativa",
                "formula": "Urx/sqrt(3)"
            }
        }
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
        ],
        "soluzione": {
            "urx": {
                "msg": "% Incertezza standard relativa",
                "formula": "sqrt((crx1*urx1)^2 + (crx2*urx2)^2 + (crphi*urphi)^2)"
            },
            "Urx": {
                "msg": "% Incertezza di caso peggiore relativa",
                "formula": "sqrt(3)*urx"
            },
            "Ux": {
                "msg": "% Incertezza di caso peggiore assoluta",
                "formula": "Urx*abs(x)"
            }
        }
    }
}