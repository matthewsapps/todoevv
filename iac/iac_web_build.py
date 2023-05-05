from troposphere import (
    ImportValue,
    GetAtt,
    Ref,
    Template,
    Join,
    Tags,
)

from troposphere.s3 import (
    Bucket,
    PublicAccessBlockConfiguration,
    BucketEncryption,
    BucketPolicy,
    ServerSideEncryptionRule,
    ServerSideEncryptionByDefault,
    CorsConfiguration,
    CorsRules,
    VersioningConfiguration,
    NotificationConfiguration,
    QueueConfigurations,
)

from troposphere.cloudfront import ( 
    Distribution, DistributionConfig, Origin, S3OriginConfig, ViewerCertificate, 
    CloudFrontOriginAccessIdentity, CloudFrontOriginAccessIdentityConfig, DefaultCacheBehavior,
    CachePolicy, CachePolicyConfig, ParametersInCacheKeyAndForwardedToOrigin, CacheCookiesConfig, 
    CacheHeadersConfig, CacheQueryStringsConfig, OriginRequestPolicy, OriginRequestHeadersConfig,
    OriginRequestCookiesConfig, OriginRequestQueryStringsConfig, ResponseHeadersPolicy, 
    ResponseHeadersPolicyConfig, CorsConfig, AccessControlAllowHeaders,AccessControlAllowMethods, 
    AccessControlAllowOrigins, OriginRequestPolicyConfig, PublicKey, PublicKeyConfig,
    KeyGroup, KeyGroupConfig
)

from troposphere.route53 import RecordSetType, AliasTarget

def main():
    t= Template()

    ssl_cert = "arn:aws:acm:us-east-1:473590191074:certificate/0d37d917-f950-423c-8407-efd8450e790e"

    website_bucket = t.add_resource(
        Bucket(
            "WebsiteBucket",
            BucketName="todoevv.matthewsapps.com",
            PublicAccessBlockConfiguration=PublicAccessBlockConfiguration(
                BlockPublicAcls=True,
                BlockPublicPolicy=True,
                IgnorePublicAcls=True,
                RestrictPublicBuckets=True
            ),
            Tags=Tags(
                { "Application": Ref("AWS::StackId") }
            )
        )
    )

    cloudfront_distro_cache_policy = t.add_resource(
        CachePolicy(
            "CloudfrontDistroCachePolicy",
            CachePolicyConfig=CachePolicyConfig(
                DefaultTTL=86400,
                MaxTTL=3153600,
                MinTTL=86400,
                Name="cloudfront-todoevv-resources-cache-policy",
                ParametersInCacheKeyAndForwardedToOrigin=ParametersInCacheKeyAndForwardedToOrigin(
                    CookiesConfig=CacheCookiesConfig(
                        CookieBehavior="none"
                    ),
                    EnableAcceptEncodingGzip=True,
                    EnableAcceptEncodingBrotli=True,
                    HeadersConfig=CacheHeadersConfig(
                        HeaderBehavior="none"
                    ),
                    QueryStringsConfig=CacheQueryStringsConfig(
                        QueryStringBehavior="none"
                    )
                )
            )
        )
    )

    cloudfront_origin_access = t.add_resource(
        CloudFrontOriginAccessIdentity(
            "CloudfrontOriginAccess",
            CloudFrontOriginAccessIdentityConfig=CloudFrontOriginAccessIdentityConfig(
                "CloudfrontOriginAccessConfig",
                Comment="To Do EVV Cloudfront Origin Access"
            )
        )
    )

    cloudfront_origin_req_policy = t.add_resource(
        OriginRequestPolicy(
            "CloudFrontOriginReqPolicy",
            OriginRequestPolicyConfig=OriginRequestPolicyConfig(
                Name="ToDoEVVCORSRequestPolicy",
                HeadersConfig=OriginRequestHeadersConfig(
                    HeaderBehavior="whitelist",
                    Headers=[
                        "origin",
                        "access-control-request-headers",
                        "access-control-request-method"
                    ]
                ),
                CookiesConfig=OriginRequestCookiesConfig(
                    CookieBehavior='none'
                ),
                QueryStringsConfig=OriginRequestQueryStringsConfig(
                    QueryStringBehavior='none'
                )
            )
        )
    )

    cloudfront_response_headers_policy = t.add_resource(
        ResponseHeadersPolicy(
            "CloudFrontResponseHeadersPolicy",
            ResponseHeadersPolicyConfig=ResponseHeadersPolicyConfig(
                Name="ToDoEVVCORSEnabled",
                CorsConfig=CorsConfig(
                    AccessControlAllowCredentials=False,
                    AccessControlAllowOrigins=AccessControlAllowOrigins(
                        Items=[
                            "https://todoevv.matthewsapps.com"
                        ]
                    ),
                    AccessControlAllowHeaders=AccessControlAllowHeaders(
                        Items=["*"]
                    ),
                    AccessControlAllowMethods=AccessControlAllowMethods(
                        Items=["GET", "OPTIONS", "HEAD"]
                    ),
                    OriginOverride=False
                )
            )
        )
    )

    resources_distro = t.add_resource(
        Distribution(
            "ResourcesCloudFrontDistro",
            DistributionConfig=DistributionConfig(
                Aliases=["todoevv.matthewsapps.com"],
                Enabled=True,
                Origins=[
                    Origin(
                        DomainName=Join('', [ Ref(website_bucket), '.s3.', Ref("AWS::Region"), '.amazonaws.com' ]),
                        Id="todoevv.matthewsapps.com",
                        S3OriginConfig=S3OriginConfig(
                            OriginAccessIdentity=Join('', [ "origin-access-identity/cloudfront/", Ref(cloudfront_origin_access) ])
                        )
                    )
                ],
                PriceClass="PriceClass_100",
                ViewerCertificate=ViewerCertificate(
                    "ViewerCert",
                    AcmCertificateArn=ssl_cert,
                    MinimumProtocolVersion="TLSv1.2_2021",
                    SslSupportMethod="sni-only"
                    # CHANGING SslSupportMethod MIGHT COST US $600/MONTH, 
                    # MAKE SURE YOU KNOW WHAT YOU ARE DOING
                ),
                DefaultCacheBehavior=DefaultCacheBehavior(
                    "DefaultCacheBehavior",
                    AllowedMethods=["GET", "HEAD", "OPTIONS"],
                    CachePolicyId=Ref(cloudfront_distro_cache_policy),
                    OriginRequestPolicyId=Ref(cloudfront_origin_req_policy),
                    ResponseHeadersPolicyId=Ref(cloudfront_response_headers_policy),
                    TargetOriginId="todoevv.matthewsapps.com",
                    ViewerProtocolPolicy="redirect-to-https"
                )
            ),
            Tags=Tags(
                { "Application": Ref("AWS::StackId") }
            )
        )
    )

    bucket_policy = t.add_resource(
        BucketPolicy(
            "CloudfrontBucketAccessPolicy",
            Bucket=Ref(website_bucket),
            PolicyDocument={
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "s3:GetObject",
                        "Effect": "Allow",
                        "Principal": { "AWS": Join('', [ "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity ", Ref(cloudfront_origin_access) ]) },
                        "Resource": Join('', [ "arn:aws:s3:::", Ref(website_bucket), "/*" ])
                    }
                ],
            }
        )
    )

    cloudfront_record = t.add_resource(
        RecordSetType(
            "RecordSet",
            AliasTarget=AliasTarget(
                DNSName=GetAtt(resources_distro, "DomainName"),
                HostedZoneId="Z2FDTNDATAQYW2"
            ),
            Type="A",
            Name="todoevv.matthewsapps.com",
            HostedZoneName="matthewsapps.com."
        )
    )

    with open('./iac/template.yaml', "w") as file:
        file.write(t.to_yaml())

if __name__ == '__main__':
    main()