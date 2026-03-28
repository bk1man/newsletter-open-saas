const { Client } = require('./dist/extensions/feishu/node_modules/@larksuiteoapi/node-sdk');

(async () => {
  const client = new Client({
    appId: 'cli_a91fd2195578dcc6',
    appSecret: 'POSPeNTc1BTfEP9D5axPfeuZh8kG77wA'
  });

  const DOC_ID = 'N34PdlXiUomVBnxp4PMcRazTnUf';
  const IMAGE_KEY = 'img_v3_02103_c990a8f5-4a2a-4338-8353-fc66a00ab7eg';

  // Get token
  const tokenResp = await client.tenant_access_token.get().catch(() => null);
  let token;
  if (tokenResp && tokenResp.data && tokenResp.data.tenant_access_token) {
    token = tokenResp.data.tenant_access_token;
  } else {
    // Use internal method
    const fs = require('fs');
    const path = require('path');
    const home = require('os').homedir();
  }

  // Get token via API
  const https = require('https');
  
  const postData = JSON.stringify({app_id: 'cli_a91fd2195578dcc6', app_secret: 'POSPeNTc1BTfEP9D5axPfeuZh8kG77wA'});
  const tokenReq = https.request({
    hostname: 'open.feishu.cn',
    path: '/open-apis/auth/v3/tenant_access_token/internal',
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'Content-Length': postData.length}
  }, (res) => {
    let d = '';
    res.on('data', c => d += c);
    res.on('end', async () => {
      token = JSON.parse(d).tenant_access_token;
      console.log('Token obtained');
      
      // Now try inserting image block
      const fetch = (...args) => import('node:fetch').then(({default: f}) => f(...args));
      
      const body = JSON.stringify({
        children: [{
          block_type: 6,
          image: {
            width: 1080,
            height: 1350,
            token: IMAGE_KEY
          }
        }],
        index: 0
      });
      
      const resp = await fetch(`https://open.feishu.cn/open-apis/docx/v1/documents/${DOC_ID}/blocks/${DOC_ID}/children`, {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body)
        },
        body
      });
      
      const result = await resp.json();
      console.log('Image insert result:', JSON.stringify(result, null, 2));
    });
  });
  tokenReq.write(postData);
  tokenReq.end();
})();
