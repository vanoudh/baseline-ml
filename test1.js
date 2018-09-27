import { Selector } from 'testcafe';

fixture `Getting Started`
    .page `http://127.0.0.1:8080`;

test('Complete new user flow', async t => {
    const n = Math.floor(Math.random() * 1000);
    const email = 'robot' + n + '@test.com';
    await t.click('#register');
    await t
        .typeText('#email_input', email)
        .typeText('#password_input', 'robot@test.com')
        .click('#register_confirm')
        .expect(Selector('#user_alert_text').innerText).eql('ok');

    await t
        .setFilesToUpload(Selector('#fileupload'), './test_data.csv')
        .click('#upload_ctn')
        .expect(Selector('#file').innerText).eql('test_data.csv');

    await t
        .click('#run')
        .expect(Selector('#zero').innerText).eql('starting...');
});