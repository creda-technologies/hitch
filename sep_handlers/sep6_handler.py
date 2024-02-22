from anchor_sdk.exceptions import MethodNotImplementedError

class Sep6Handler:
    
    def info(self):
        raise MethodNotImplementedError("sep6", "info")

    def deposit(self):
        raise MethodNotImplementedError("sep6", "deposit")

    def withdraw(self):
        raise MethodNotImplementedError("sep6", "withdraw")

    def deposit_exchange(self):
        raise MethodNotImplementedError("sep6", "deposit-exchange")

    def withdraw_exchange(self):
        raise MethodNotImplementedError("sep6", "withdraw-exchange")
    
    def fee(self):
        raise MethodNotImplementedError("sep6", "fee")
    
    def transactions(self):
        raise MethodNotImplementedError("sep6", "transactions")

    def transaction(self):
        raise MethodNotImplementedError("sep6", "transaction")

