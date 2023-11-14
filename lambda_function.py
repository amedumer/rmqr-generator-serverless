import json
import boto3
import rmqrcode
from rmqrcode import QRImage, rMQR, ErrorCorrectionLevel, FitStrategy

def lambda_handler(event, context):
    try:
        # Extracting request variables
        data = event.get('data', None)
        size = event.get('size', 'balanced').lower()
        ecc_level = event.get('error_correction_level', 'auto').upper()

        # Validate data
        if not data:
            raise ValueError("Data cannot be empty.")
        if len(data) > 200:
            raise ValueError("Data can be 200 characters maximum.")

        # Mapping size and error correction level to rmqrcode enums
        fit_strategy_map = {
            'minimize_height': FitStrategy.MINIMIZE_HEIGHT,
            'minimize_width': FitStrategy.MINIMIZE_WIDTH,
            'balanced': FitStrategy.BALANCED
        }
        ecc_map = {
            'M': ErrorCorrectionLevel.M,
            'H': ErrorCorrectionLevel.H,
            'AUTO': ErrorCorrectionLevel.M  # Defaulting to 'M' when 'auto' is chosen
        }

        # Validate fit_strategy and ecc
        fit_strategy = fit_strategy_map.get(size)
        ecc = ecc_map.get(ecc_level)
        if fit_strategy is None:
            raise ValueError(f"Invalid size value: {size}. Valid values are: {', '.join(fit_strategy_map.keys())}.")
        if ecc is None:
            raise ValueError(f"Invalid error_correction_level value: {ecc_level}. Valid values are: {', '.join(ecc_map.keys())}.")

        # Generating rMQR Code
        qr = rMQR.fit(data, ecc=ecc, fit_strategy=fit_strategy)

        # Saving as image
        image = QRImage(qr, module_size=8)
        
        # Convert to base64 and return in the response
        import io
        import base64
        buffer = io.BytesIO()
        image._img.save(buffer, format='PNG')  # Access the underlying PIL.Image object and specify the format explicitly here
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return {
            'statusCode': 200,
            'body': json.dumps({
                'rmqr_image_base64': img_str
            })
        }

    except Exception as e:
        # Logging the exception
        print(f"An error occurred: {e}")

        # Returning a 500 Internal Server Error response with the error message
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
