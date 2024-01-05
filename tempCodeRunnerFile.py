                        if wallet.value - bet.value > 0:
                            bet.display.add_changes([{"type":"text","value":f"$ {bet.value}","delay":0}])
                        else:
                            bet.display.add_changes([{"type":"text","value":f"$ {wallet.value}","delay":0}])