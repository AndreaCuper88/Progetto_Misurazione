CASES = {
    1: {
        "nome": "Assoluto - WCU",
        "tipo_input": "abs_wcu", #incertezze assolute di caso peggiore
        "tipo_propagazione": "wcu",
        "tipo_input_testuale": {
            "Ux1":      "incertezza di caso peggiore assoluta su x1",
            "Ux2":      "incertezza di caso peggiore assoluta su x2",
            "Uphi_deg": "incertezza di caso peggiore assoluta su phi (in gradi)",
        },
        "domande": [
            "cx1",
            "cx2",
            "Ux",
            "Urx",
            "ux",
            "crphi"
        ],
        "soluzione": {
            "Utheta": {
                "msg": "% Incertezza di caso peggiore assoluta",
                "formula": "abs(cx1)*Ux1 + abs(cx2)*Ux2 + abs(cphi)*Uphi"
            },
            "Urtheta": {
                "msg": "% Incertezza di caso peggiore relativa",
                "formula": "Utheta/abs(theta)"
            },
            "utheta": {
                "msg": "% Incertezza standard assoluta",
                "formula": "Utheta/sqrt(3)"
            }
        }
    },

    2: {
        "nome": "Assoluto - Standard",
        "tipo_input": "abs_std",    #incertezze assolute standard
        "tipo_propagazione": "std",
        "tipo_input_testuale": {
            "ux1":      "incertezza standard assoluta su x1",
            "ux2":      "incertezza standard assoluta su x2",
            "uphi_deg": "incertezza standard assoluta su phi (in gradi)",
        },
        "domande": [
            "cx1",
            "cx2",
            "Ux",
            "Urx",
            "ux",
            "crphi"
        ],
        "soluzione": {
            "utheta": {
                "msg": "% Incertezza standard assoluta",
                "formula": "sqrt((cx1*ux1)^2 + (cx2*ux2)^2 + (cphi*uphi)^2)"
            },
            "Utheta": {
                "msg": "% Incertezza di caso peggiore assoluta",
                "formula": "sqrt(3)*utheta"
            },
            "Urtheta": {
                "msg": "% Incertezza di caso peggiore relativa",
                "formula": "Utheta/abs(theta)"
            }
        }
    },

    3: {
        "nome": "Relativo - WCU",
        "tipo_input": "rel_wcu",    #incertezze relative di caso peggiore
        "tipo_propagazione": "wcu",
        "tipo_input_testuale": {
            "Urx1":     "incertezza di caso peggiore relativa su x1",
            "Urx2":     "incertezza di caso peggiore relativa su x2",
            "Uphi_deg": "incertezza di caso peggiore assoluta su phi (in gradi)",
        },
        "domande": [
            "crx1",
            "crx2",
            "Urx",
            "Ux",
            "urx",
            "cphi"
        ],
        "soluzione": {
            "Urtheta": {
                "msg": "% Incertezza di caso peggiore relativa",
                "formula": "abs(crx1)*Urx1 + abs(crx2)*Urx2 + abs(crphi)*Urphi"
            },
            "Utheta": {
                "msg": "% Incertezza di caso peggiore assoluta",
                "formula": "Urtheta*abs(theta)"
            },
            "urtheta": {
                "msg": "% Incertezza standard relativa",
                "formula": "Urtheta/sqrt(3)"
            }
        }
    },

    4: {
        "nome": "Relativo - Standard",
        "tipo_input": "rel_std",    #incertezze relative standard
        "tipo_propagazione": "std",
        "tipo_input_testuale": {
            "urx1":     "incertezza standard relativa su x1",
            "urx2":     "incertezza standard relativa su x2",
            "uphi_deg": "incertezza standard assoluta su phi (in gradi)",
        },
        "domande": [
            "crx1",
            "crx2",
            "Urx",
            "Ux",
            "urx",
            "cphi"
        ],
        "soluzione": {
            "urtheta": {
                "msg": "% Incertezza standard relativa",
                "formula": "sqrt((crx1*urx1)^2 + (crx2*urx2)^2 + (crphi*urphi)^2)"
            },
            "Urtheta": {
                "msg": "% Incertezza di caso peggiore relativa",
                "formula": "sqrt(3)*urtheta"
            },
            "Utheta": {
                "msg": "% Incertezza di caso peggiore assoluta",
                "formula": "Urtheta*abs(theta)"
            }
        }
    }
}