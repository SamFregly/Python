import vcf
import sys

vcf_reader = vcf.Reader(open("/home/sam/Downloads/VCF.vcf",'r'))
vcf_file = open('vcfoutput.vcf', 'a')
for record in vcf_reader:
	data = str(record.INFO)
	dp4 = record.INFO["DP4"]
	if "missense_variant" in data and dp4[0] >= 15000:
		vcf_file.write(str(record))
		vcf_file.write('\n')
