import { Selector } from 'testcafe';

// fixture `Baseline ML local`.page `http://127.0.0.1:8080`;
fixture `Getting Started`.page `https://baseline-ml.appspot.com`;


test('new user complete flow', async t => {
    
    await t
        .click('#register')
        .typeText('#email_input', 'robot1@testcafe.com')
        .typeText('#password_input', '12345678')
        .typeText('#first_name_input', 'robot1')
        .typeText('#last_name_input', 'testcafe')
        .click('#register_confirm')
        .expect(Selector('#user_alert_text').innerText).eql('ok');

    await t
        .wait(2000)
        .setFilesToUpload(Selector('#fileupload'), './test_data.csv')
        .click('#upload_ctn')
        .wait(2000)
        .expect(Selector('#file').innerText).eql('test_data.csv');

    await t
        .click('#PassengerIdi')
        .click('#Survivedt')
        .click('#run')
        .expect(Selector('#linear').innerText).eql('starting...')
        .wait(30000)
        .expect(Selector('#zero'  ).innerText).eql('0.65')
        .expect(Selector('#linear').innerText).eql('0.9')
        .expect(Selector('#tree'  ).innerText).eql('0.8')
        .expect(Selector('#forest').innerText).eql('0.8');
    
    await t
        .click('#delete')
        .wait(1000)
        .expect(Selector('#file').innerText).eql('---');
});


test('register login logout delete', async t => {
    
    await t
        .click('#register')
        .typeText('#email_input', 'robot2@testcafe.com')
        .typeText('#password_input', '12345678')
        .typeText('#first_name_input', 'robot2')
        .typeText('#last_name_input', 'testcafe')
        .click('#register_confirm')
        .expect(Selector('#user_alert_text').innerText).eql('ok')
        .expect(Selector('#file').innerText).eql('You have no file yet');
    
    await t
        .click('#logout')
        .expect(Selector('#file').innerText).eql('---');

    await t
        .typeText('#email_input', 'robot2@testcafe.com')
        .typeText('#password_input', '12345678x')
        .click('#login')
        .expect(Selector('#user_alert_text').innerText).eql('Login failed')
        .expect(Selector('#file').innerText).eql('---');

    await t.eval(() => location.reload(true));

    await t
        .click('#register')
        .typeText('#email_input', 'robot2@testcafe.com')
        .typeText('#password_input', '87654321')
        .typeText('#first_name_input', 'robot2')
        .typeText('#last_name_input', 'testcafe')
        .click('#register_confirm')
        .expect(Selector('#user_alert_text').innerText).eql('User already registered')
        .expect(Selector('#file').innerText).eql('---');

    await t.eval(() => location.reload(true));

    await t
        .typeText('#email_input', 'robot2@testcafe.com')
        .typeText('#password_input', '12345678')
        .click('#login')
        .expect(Selector('#user_alert_text').innerText).eql('ok');

    await t
        .click('#delete')
        .expect(Selector('#file').innerText).eql('---');
});


test('email password rules', async t => {
    
    await t
        .click('#login')
        .expect(Selector('#user_alert_text').innerText).eql('Invalid email')
        .expect(Selector('#file').innerText).eql('---');

    await t
        .typeText('#email_input', 'robot3@testcafe.com')
        .typeText('#password_input', '1234567')
        .click('#login')
        .expect(Selector('#user_alert_text').innerText).eql('Password should be at least 8 characters')
        .expect(Selector('#file').innerText).eql('---');
});
