require 'openssl'

KEY_LENGTH = 8 # TODO

def generate_key(seed)
  key = ""
  1.upto(KEY_LENGTH) do
    seed = (214013 * seed + 2531011)
    key += (((seed>>16) & 0x7fff_ffff) & 0x0FF).chr
    #print key.unpack('H*')
  end

  return key
end


def cbcD(data,key)
    c = OpenSSL::Cipher::DES.new('CBC')
    c.decrypt
    c.key = key
    return (c.update(data) + c.final())
end
filepdf = File.open("ElfUResearchLabsSuperSledOMaticQuickStartGuideV1.2.pdf.enc", "rb")
contents = filepdf.read
filepdf.close
i = 1575658800
    while i<=1575666001 do
        key = generate_key(i)
        begin
            maydata=cbcD(contents,key)
            puts "#{key.unpack('H*')}"
            name= "foundit"+i.to_s + ".pdf"
            File.write(name,maydata)
            
        rescue
            puts "#{key.unpack('H*')} seed is wroooong"
	    end
        
    i += 1
    end
    

