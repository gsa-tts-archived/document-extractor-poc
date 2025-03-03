locals {
  s3_origin_id          = "website-in-s3"
  api_gateway_origin_id = "api-in-gateway"
  api_prefix_path       = "api"
}

resource "aws_cloudfront_distribution" "distribution" {
  enabled = true
  comment = "${local.project} ${var.environment} website"

  http_version    = "http2"
  is_ipv6_enabled = true
  price_class     = "PriceClass_100"

  origin {
    domain_name = aws_s3_bucket_website_configuration.website_configuration.website_endpoint
    origin_id   = local.s3_origin_id

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  origin {
    domain_name = split("/", aws_api_gateway_deployment.api_deployment.invoke_url)[2] # grabs the domain name from something like this `https://asdf.execute-api.us-east-1.amazonaws.com/`
    origin_id   = local.api_gateway_origin_id
    origin_path = "/${aws_api_gateway_stage.stage.stage_name}"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]

    target_origin_id       = local.s3_origin_id
    viewer_protocol_policy = "redirect-to-https"

    default_ttl = 86400  #one day
    max_ttl     = 172800 #two days
    compress    = true

    forwarded_values {
      cookies {
        forward = "none"
      }

      query_string = false
    }
  }

  ordered_cache_behavior {
    path_pattern           = "/${local.api_prefix_path}/*"
    target_origin_id       = local.api_gateway_origin_id
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
    cached_methods         = ["GET", "HEAD"]

    cache_policy_id          = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad" // CachingDisabled
    origin_request_policy_id = "b689b0a8-53d0-40ab-baf2-68738e2966ac" // AllViewerExceptHostHeader

    compress = true

    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.rewrite_uri.arn
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}

# Remove the beginning /api from the request.
# This changes /api/dogcow/moof at CloudFront to /dogcow/moof at the origin.
# This is needed to make the API gateway accept the request.
resource "aws_cloudfront_function" "rewrite_uri" {
  name    = "${local.project}-${var.environment}-rewrite-request"
  runtime = "cloudfront-js-1.0"
  code    = <<EOF
function handler(event) {
	var request = event.request;
	request.uri = request.uri.replace(/^\/${local.api_prefix_path}\//, "/");
	return request;
}
EOF
}
