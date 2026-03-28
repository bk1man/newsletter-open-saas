const { Client } = require('/root/.nvm/versions/node/v22.22.1/lib/node_modules/openclaw/dist/extensions/feishu/node_modules/@larksuiteoapi/node-sdk');
const fs = require('fs');

const client = new Client({
  appId: 'cli_a91fd2195578dcc6',
  appSecret: 'POSPeNTc1BTfEP9D5axPfeuZh8kG77wA'
});

const date = process.argv[2] || new Date().toISOString().slice(0,10);
const imgPath = `/root/newsletter/social/post_${date}.png`;

if (!fs.existsSync(imgPath)) {
  console.log(`Image not found: ${imgPath}`);
  process.exit(1);
}

const fileStream = fs.createReadStream(imgPath);

client.im.image.create({
  data: {
    image_type: 'message',
    image: fileStream
  }
}).then(async r => {
  const imageKey = r.image_key;
  console.log('Image uploaded:', imageKey);
  
  const result = await client.im.message.create({
    data: {
      receive_id: 'ou_d0142c3276f28f0bdea6f604fac0c1e1',
      msg_type: 'image',
      content: JSON.stringify({ Image_key: imageKey })
    },
    params: { receive_id_type: 'open_id' }
  });
  
  console.log('Sent! Message ID:', result.data?.message_id);
}).catch(e => {
  console.log('Error:', e.message);
  if(e.response) console.log('Response:', JSON.stringify(e.response.data));
});
