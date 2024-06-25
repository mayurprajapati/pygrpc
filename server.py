import grpc
from concurrent import futures
import python_bridge_pb2
import python_bridge_pb2_grpc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_recaptcha_solver import RecaptchaSolver


class CalculatorServicer(python_bridge_pb2_grpc.PythonBridgeServicer):
    def resolveRecaptcha(self, request, context):
        ip = request.ip
        port = request.port
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", f"{ip}:{port}")
        driver = webdriver.Chrome(options=chrome_options)
        recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
        solver = RecaptchaSolver(driver=driver)
        solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        return python_bridge_pb2.CommonResponse(success=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    python_bridge_pb2_grpc.add_PythonBridgeServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
