
import re

pattern = r'[(（\[【]\d{4}[】\]）)][^\d]*第?[\d]+号(?:、第?[\d]+号)*'
pattern = r'[(（\[【]\d{4}[】\]）)][^.。，,号]*第?[\d]+号?(?:、第?[\d]+号?)*'

texts = [
    '在曲靖中院（2012）曲中法执字第66号、第106号案件中处置的剩余款项',
    '白云区人民法院（2021）粤0111民初30063、30062、30064号民事判决',
    '在曲靖中院（2012）曲中法执字第66号案件中处置的剩余款项'
]

for text in texts:
    match = re.search(pattern, text)
    if match:
        print(match.group(0))
