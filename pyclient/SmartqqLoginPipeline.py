import io
from .GetBarcodeStepHandler import GetBarcodeStepHandler
from .GetPsessionidHandler import GetPsessionidHandler
from .GetPtwebqqHandler import GetPtwebqqHandler
from .GetVfwebqqHandler import GetVfwebqqHandler
from .LoginPipeline import LoginPipeline
from .WaitForAuthHandler import WaitForAuthHandler
from .LoginFinalizeHandler import LoginFinalizeHandler


class SmartqqLoginPipeline(LoginPipeline):
    def __init__(self, session, barcode_handler=None):
        super().__init__(session)
        if barcode_handler is None:

            def barcode_store(barcode: io.BytesIO):
                with open("barcode.png", "wb") as barcode_file:
                    import shutil
                    shutil.copyfileobj(barcode, barcode_file)
                    print("Please scan the barcode png to login")
                    barcode.seek(0)

            self.barcode_handler = barcode_store
        else:
            self.barcode_handler = barcode_handler
        self.add_step(GetBarcodeStepHandler(session))
        self.add_step(WaitForAuthHandler(session, barcode_handler=self.barcode_handler))
        self.add_step(GetPtwebqqHandler(session))
        self.add_step(GetVfwebqqHandler(session))
        self.add_step(GetPsessionidHandler(session))
        self.add_step(LoginFinalizeHandler(session))
