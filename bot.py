const { Client, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

const client = new Client();

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('Client is ready!');
});

client.on('message', async msg => {
    if (msg.hasMedia) {
        const media = await msg.downloadMedia();

        // Hanya menyimpan foto sekali lihat
        if (msg.type === 'image' && msg.isViewOnce) {
            const mediaPath = path.join(__dirname, 'media');

            if (!fs.existsSync(mediaPath)) {
                fs.mkdirSync(mediaPath);
            }

            const filePath = path.join(mediaPath, `photo_${Date.now()}.jpeg`);

            fs.writeFile(filePath, media.data, { encoding: 'base64' }, (err) => {
                if (err) {
                    console.error('Failed to save the image:', err);
                } else {
                    console.log('Image saved successfully:', filePath);
                }
            });
        }
    }
});

client.initialize();
