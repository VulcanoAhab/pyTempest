import os
import json
from smallBoto import S3Buket
from streamparse import Bolt

class S3IN(Bolt):
    """
    """
    def initialize(self, conf, ctx):
        """
        """
        self.pid = os.getpid()
        S3Buket.basic_conn=(access_key=os.env.get("ACCESS_KEY"),
                            secret_key=os.env.get("SECRET_KEY"))
    def process(self, tup):
        """
        tup:("bucketName", "key", "fileData", "metadata")
        """
        self.logger.info("[+] STARTING S3")
        bucketName, key, fileData, metadata=tup.values()
        bucket=S3Bucket(bucketName)
        #prepare data
        fileData=json.dumps(fileData).encode()
        #upload DATA
        bucket.uploadFileData(fileData, key)
        loadMessage="[+] Loaded {} bites to {}:{}".format(dataLen,
                                                    key,bucketName)
        self.logger.info(loadMessage)
