## Overview

This AWS Lambda function is a Python-based microservice for generating Rectangular Micro QR (rMQR) codes with the API. Specify data, size preference, and error correction level to get a customized rMQR code. Ideal for space-constrained or unique design applications, get a fast, reliable, and easy-to-integrate solution for your rMQR code generation needs.

# rMQR Code Generation API

Generate Rectangular Micro QR (rMQR) codes on-the-go with our simple yet powerful API. Tailored for space-constrained or unique design applications, it's now easier than ever to integrate rMQR code generation in your projects.

## Endpoint

`POST /generate-rmqr`

## Request Parameters

- `data` (string, required): The data to be encoded in the rMQR code. Max 200 characters.
- `size` (string, optional, default: "balanced"): The size preference for the rMQR code. Acceptable values are:
  - `minimize_height`
  - `minimize_width`
  - `balanced`
- `error_correction_level` (string, optional, default: "auto"): The error correction level for the rMQR code. Acceptable values are:
  - `M`
  - `H`
  - `auto` (defaults to `M`)

## Example Request

```json
{
  "data": "https://example.com",
  "size": "balanced",
  "error_correction_level": "M"
}
```

## Response

The API responds with a JSON object containing the base64-encoded PNG image of the generated rMQR code.

- rmqr_image_base64 (string): The base64-encoded PNG image of the generated rMQR code.

## Example Response

```json
{
  "rmqr_image_base64": "iVBORw…"
}
```

## Error Handling

In case of an error, the API will return a 500 Internal Server Error status code along with a JSON object containing an error key with a string value describing the error.

## Example Error Response

```json
{
  "error": "Data cannot be empty."
}
```
