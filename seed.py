from app import app
from models import db, Bag, Cap, Tshirt
from flask_bcrypt import Bcrypt

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all() 

bags = [
    Bag(name='Brent Faiyaz bag 1',inspiration='Brent Faiyaz', price=550, image='https://i.pinimg.com/736x/e3/f0/a7/e3f0a77e991d6f1588428ccefc2eba92.jpg'),
    Bag(name='Brent Faiyaz bag 2',inspiration='Brent Faiyaz', price=550, image='https://i.pinimg.com/736x/e4/e7/25/e4e7250cab29310dbb360a3bf5e02f96.jpg'),
    Bag(name='Brent Faiyaz bag 3',inspiration='Brent Faiyaz', price=550, image='https://i.pinimg.com/736x/10/d3/cf/10d3cf92fedeca43a001324d5438947f.jpg'),
    Bag(name='Brent Faiyaz bag 4',inspiration='Brent Faiyaz', price=550, image='https://i.pinimg.com/736x/f1/42/5a/f1425a727b67e2b37ab4775f444ce5e2.jpg'),
    Bag(name='Brent Faiyaz bag 5',inspiration='Brent Faiyaz', price=550, image='https://i.pinimg.com/736x/70/e0/c6/70e0c6edb21d8c7b3ac59bf742caf68e.jpg'),
    Bag(name='Brent Faiyaz bag 6',inspiration='Brent Faiyaz', price=550, image='https://i.pinimg.com/736x/5d/9a/2e/5d9a2eb7b9eb7c86388d47c3fa109f14.jpg'),
    Bag(name='Brent Faiyaz bag 7',inspiration='Brent Faiyaz', price=550, image='https://i.pinimg.com/736x/b7/27/2f/b7272fc4bcfe0913dc5fd431ea2521d1.jpg'),
    Bag(name='Brent Faiyaz bag 8',inspiration='Brent Faiyaz', price=550, image='https://i.pinimg.com/736x/ae/d8/3a/aed83af2b20b69d7a2405aa43988d3ef.jpg'),
    Bag(name='Brent Faiyaz bag 9',inspiration='Brent Faiyaz', price=550, image='https://i.pinimg.com/736x/af/fa/12/affa12dbe54d8b0656e7a6537746b8e9.jpg'),
    # Bag(name='Brent Faiyaz bag 10',inspiration='Brent Faiyaz', price=550, image='https://example.com/bag10.jpg'),
    # Bag(name='Brent Faiyaz bag 11',inspiration='Brent Faiyaz', price=550, image='https://example.com/bag11.jpg'),
    Bag(name='Kendrick Lamar bag 1',inspiration='Kendrick Lamar', price=550, image='https://i.pinimg.com/736x/66/75/37/667537fe7aeba3da4b7155d5072362b2.jpg'),
    Bag(name='Kendrick Lamar bag 2',inspiration='Kendrick Lamar', price=550, image='https://i.pinimg.com/736x/74/04/90/7404902405093fdd949ec7b05b9fe900.jpg'),
    Bag(name='Kendrick Lamar bag 3',inspiration='Kendrick Lamar', price=550, image='https://i.pinimg.com/736x/7d/b1/c8/7db1c8ea5cec613410c2f228cd1a75a3.jpg'),
    Bag(name='Kendrick Lamar bag 4',inspiration='Kendrick Lamar', price=550, image='https://i.pinimg.com/736x/c5/e8/ba/c5e8ba56a98db99b65ebe0e7b2e953a2.jpg'),
    Bag(name='Kendrick Lamar bag 5',inspiration='Kendrick Lamar', price=550, image='https://i.pinimg.com/736x/bd/dd/76/bddd76e6fb324253932ca7f99eef983e.jpg'),
    Bag(name='Kendrick Lamar bag 6',inspiration='Kendrick Lamar', price=550, image='https://i.pinimg.com/736x/bb/4c/0e/bb4c0eaab464c76dd5919b5b9ebcf6e5.jpg'),
    Bag(name='Kendrick Lamar bag 7',inspiration='Kendrick Lamar', price=550, image='https://i.pinimg.com/736x/64/3a/21/643a21e15d1996d5178d25ecd25e100b.jpg'),
    Bag(name='Kendrick Lamar bag 8',inspiration='Kendrick Lamar', price=550, image='https://i.pinimg.com/736x/81/f2/2d/81f22d96ba407b9a2a2fe83e6b16cde5.jpg'),
    Bag(name='Kendrick Lamar bag 9',inspiration='Kendrick Lamar', price=550, image='https://i.pinimg.com/736x/48/ab/cd/48abcd7ecfed5585195ea38b18edc737.jpg'),
    Bag(name='Kendrick Lamar bag 10',inspiration='Kendrick Lamar', price=550, image='https://i.pinimg.com/736x/b2/83/b3/b283b3c9b4a951a03e4b2b5de15a715d.jpg'),
    Bag(name='Drake bag 1',inspiration='Drake', price=550, image='https://i.pinimg.com/474x/e2/52/e4/e252e4560d8d6092847626aa0af7a088.jpg'),
    Bag(name='Drake bag 2',inspiration='Drake', price=550, image='https://i.pinimg.com/474x/28/08/1c/28081c7898d7572543d6815d9df21582.jpg'),
    Bag(name='Drake bag 3',inspiration='Drake', price=550, image='https://i.pinimg.com/474x/30/4f/bc/304fbc5e7203db3ecc925adf1007882b.jpg'),
    Bag(name='Drake bag 4',inspiration='Drake', price=550, image='https://i.pinimg.com/474x/92/35/32/923532b1c9cc1e2c399a9aa5c449a8bd.jpg'),
    Bag(name='Drake bag 5',inspiration='Drake', price=550, image='https://i.pinimg.com/474x/df/1f/49/df1f490accddbd6ab5ac07f01c9c6e17.jpg'),
    Bag(name='Drake bag 6',inspiration='Drake', price=550, image='https://i.pinimg.com/474x/ca/c6/7a/cac67a08d3cdcb5964826e804f6ed303.jpg'),
    Bag(name='Drake bag 7',inspiration='Drake', price=550, image='https://i.pinimg.com/474x/6b/b1/a9/6bb1a938aada787b0b8aca22791c0e0c.jpg'),
    Bag(name='Drake bag 8',inspiration='Drake', price=550, image='https://i.pinimg.com/474x/b9/e5/4e/b9e54ec0db29f893875d785c8c28507d.jpg'),
    Bag(name='Drake bag 9',inspiration='Drake', price=550, image='https://i.pinimg.com/474x/62/20/2a/62202a9a2fcc81521d3bc7ee53dfff9b.jpg'),
    Bag(name='Drake bag 10',inspiration='Drake', price=550, image='https://i.pinimg.com/474x/98/7e/87/987e87405bf64e9b982d0d4ef82e95a8.jpg'),
    Bag(name='Drake bag 11',inspiration='Drake', price=550, image='https://i.pinimg.com/736x/66/ea/d1/66ead1922ed3bef620653c987d71c089.jpg'),
    Bag(name='Drake bag 12',inspiration='Drake', price=550, image='https://i.pinimg.com/474x/b5/11/3d/b5113d8224b36b48bec1ad55ac8fdb52.jpg'),
    Bag(name='Drake bag 13',inspiration='Drake', price=550, image='https://i.pinimg.com/736x/d7/9c/bd/d79cbd1890b77e1fa97beb63d8334b69.jpg'),
    Bag(name='Drake bag 14',inspiration='Drake', price=550, image='https://i.pinimg.com/736x/79/eb/3c/79eb3c1997daa232e7e8c12b25379d56.jpg'),
    Bag(name='Drake bag 15',inspiration='Drake', price=550, image='https://i.pinimg.com/736x/9e/33/42/9e3342810a3bd90c21d77509953f3a48.jpg'),
    Bag(name='Drake bag 16',inspiration='Drake', price=550, image='https://i.pinimg.com/736x/c3/30/a3/c330a3cbd98e9149b0b5befeeb9f0932.jpg'),
    # Bag(name='Drake bag 17',inspiration='Drake', price=550, image='https://example.com/bag38.jpg'),
    Bag(name='Burna Boy bag 1',inspiration='Burna Boy', price=550, image='https://i.pinimg.com/736x/5a/bb/3a/5abb3a83d44d04a9970b0fddb0397562.jpg'),
    Bag(name='Burna Boy bag 2',inspiration='Burna Boy', price=550, image='https://i.pinimg.com/736x/ee/b7/27/eeb727cd2935ef35b3610b78480effc2.jpg'),
    Bag(name='Burna Boy bag 3',inspiration='Burna Boy', price=550, image='https://i.pinimg.com/736x/bd/a7/64/bda764c13c6a8eac3ec070d5bc0612c2.jpg'),
    Bag(name='Burna Boy bag 4',inspiration='Burna Boy', price=550, image='https://i.pinimg.com/736x/c0/93/74/c09374bb114f0bc71f6534dae80c6f58.jpg'),
    Bag(name='Burna Boy bag 5',inspiration='Burna Boy', price=550, image='https://i.pinimg.com/736x/5f/d3/1d/5fd31d501630feff90110500c2a0465d.jpg'),   
    Bag(name='Burna Boy bag 6',inspiration='Burna Boy', price=550, image='https://i.pinimg.com/736x/ce/c9/2e/cec92e7948f95de2c33a1f05ccbff8dc.jpg'),
    Bag(name='Burna Boy bag 7',inspiration='Burna Boy', price=550, image='https://i.pinimg.com/736x/3f/fd/3b/3ffd3bb394543cdac75c1aff037bba8b.jpg'),
    Bag(name='Burna Boy bag 8',inspiration='Burna Boy', price=550, image='https://i.pinimg.com/736x/a1/1d/47/a11d47fac3ffe4a858fed4bbdb0e22b0.jpg'),
    Bag(name='Burna Boy bag 9',inspiration='Burna Boy', price=550, image='https://i.pinimg.com/736x/4b/99/a7/4b99a7b1656af4493aa62778298e7313.jpg'),
    Bag(name='SZA bag 1',inspiration='SZA', price=550, image='https://i.pinimg.com/736x/ef/94/b3/ef94b362376f51f25b6475ad2949525c.jpg'),
    Bag(name='SZA bag 2',inspiration='SZA', price=550, image='https://i.pinimg.com/736x/8c/cc/de/8cccded0320379904724a7a598687284.jpg'),
    Bag(name='SZA bag 3',inspiration='SZA', price=550, image='https://i.pinimg.com/736x/9b/b3/c2/9bb3c263fbe89c31a9aa1d3530c6b105.jpg'),
    Bag(name='SZA bag 4',inspiration='SZA', price=550, image='https://i.pinimg.com/736x/c9/70/1f/c9701f6985832dbb16b8ddbd0c20d041.jpg'),
    Bag(name='SZA bag 5',inspiration='SZA', price=550, image='https://i.pinimg.com/736x/48/93/37/489337fcd7b1a92f70f35f0f75bd5772.jpg'),
    Bag(name='SZA bag 6',inspiration='SZA', price=550, image='https://i.pinimg.com/736x/11/5e/0b/115e0bea65eb2106ab65c12f3943cb1f.jpg'),
    Bag(name='Frank Ocean bag 1',inspiration='Frank Ocean', price=550, image='https://i.pinimg.com/474x/b3/6a/8d/b36a8d8e65dc2c830929c465925e5e39.jpg'),
    Bag(name='Frank Ocean bag 2',inspiration='Frank Ocean', price=550, image='https://i.pinimg.com/474x/88/73/c2/8873c2deb070581eb361361dba91b562.jpg'),
    Bag(name='Frank Ocean bag 3',inspiration='Frank Ocean', price=550, image='https://i.pinimg.com/474x/4e/4a/6f/4e4a6f6150728a75dfbccefb2a6dcc6c.jpg'),
    Bag(name='Frank Ocean bag 4',inspiration='Frank Ocean', price=550, image='https://i.pinimg.com/474x/ff/6d/84/ff6d84761a63be7837d5a5cc0653e14d.jpg'),
    Bag(name='Frank Ocean bag 5',inspiration='Frank Ocean', price=550, image='https://i.pinimg.com/474x/15/e7/b5/15e7b55f3759c3c33f2209c40e225549.jpg'),
    Bag(name='Playboi Carti bag 1',inspiration='Playboi Carti', price=550, image='https://i.pinimg.com/736x/29/d6/56/29d6565c63779411236c30e4f233c7de.jpg'),
    Bag(name='Playboi Carti bag 2',inspiration='Playboi Carti', price=550, image='https://i.pinimg.com/736x/ec/ef/85/ecef858f9ea4fd3cdf46a40a1cb1c471.jpg'),
    Bag(name='Playboi Carti bag 3',inspiration='Playboi Carti', price=550, image='https://i.pinimg.com/736x/0a/ed/40/0aed40d4ca94eb88838f618a75253bce.jpg'),
    Bag(name='Playboi Carti bag 4',inspiration='Playboi Carti', price=550, image='https://i.pinimg.com/736x/57/8f/59/578f5998eb5b4166a69656e4af105f17.jpg'),
    Bag(name='Lauryn Hill bag 1',inspiration='Lauryn Hill', price=550, image='https://i.pinimg.com/736x/60/3e/16/603e161a79b9d827b49663c7cf147964.jpg'),
    Bag(name='Lauryn Hill bag 2',inspiration='Lauryn Hill', price=550, image='https://i.pinimg.com/736x/4c/e7/0d/4ce70d4e976e30d3681a12f3c9e13a76.jpg'),
    Bag(name='Lauryn Hill bag 3',inspiration='Lauryn Hill', price=550, image='https://i.pinimg.com/736x/0c/9e/c0/0c9ec0fd5d272932beacc596186065c2.jpg'),
    Bag(name='Lauryn Hill bag 4',inspiration='Lauryn Hill', price=550, image='https://i.pinimg.com/736x/f3/30/9e/f3309e5983c6e5aa8ace57f89f5856d4.jpg'),
    Bag(name='Lauryn Hill bag 5',inspiration='Lauryn Hill', price=550, image='https://i.pinimg.com/736x/90/78/ff/9078ffada8bcee7cc668450a0a10c6ca.jpg'),
    Bag(name='Lauryn Hill bag 6',inspiration='Lauryn Hill', price=550, image='https://i.pinimg.com/736x/ec/ed/19/eced19519a208ce54fb4d93724d17a8d.jpg'),
    Bag(name='Lauryn Hill bag 7',inspiration='Lauryn Hill', price=550, image='https://i.pinimg.com/736x/61/38/fb/6138fb358f4c01d576dbfd350abfaf94.jpg'),
    Bag(name='The Weeknd bag 1',inspiration='The Weeknd', price=550, image='https://i.pinimg.com/736x/ef/b9/a5/efb9a53bdc0712dcbe1e1d8ca1cf8431.jpg'),
    Bag(name='The Weeknd bag 2',inspiration='The Weeknd', price=550, image='https://i.pinimg.com/736x/1e/a7/93/1ea7939ce10c386a44921fc7ef54b38b.jpg'),
    Bag(name='The Weeknd bag 3',inspiration='The Weeknd', price=550, image='https://i.pinimg.com/736x/2c/7d/7d/2c7d7d965d71b023d0f74f978fd30c37.jpg'),
    Bag(name='The Weeknd bag 4',inspiration='The Weeknd', price=550, image='https://i.pinimg.com/736x/c8/42/d4/c842d4a31a65807467a3c9d3c0b5f625.jpg'),
    Bag(name='The Weeknd bag 5',inspiration='The Weeknd', price=550, image='https://i.pinimg.com/736x/2f/25/50/2f25503c0b5806225e5afea0d870fa92.jpg'),
    Bag(name='The Weeknd bag 6',inspiration='The Weeknd', price=550, image='https://i.pinimg.com/736x/a9/ff/50/a9ff50b7ec64f3e7b84a34807804808d.jpg'),
    Bag(name='Sade bag 1', inspiration='Sade', price=550, image='https://i.pinimg.com/736x/9e/09/55/9e09555166dd33b3e8672b585bac225c.jpg'),
    Bag(name='Tyler The Creator bag 1', inspiration='Tyler The Creator', price=550, image='https://i.pinimg.com/736x/30/66/ad/3066adbd790373104e37db02cd9cd981.jpg'),
    Bag(name='Tyler The Creator bag 2', inspiration='Tyler The Creator', price=550, image='https://i.pinimg.com/736x/27/95/a6/2795a643fa757409c03fdd84df56fa8d.jpg'),
    Bag(name='F1 bag 1', inspiration='F1', price=550, image='https://i.pinimg.com/736x/72/8d/b6/728db6dc1c75e82378e2e3f5fe4527f4.jpg'),
    Bag(name='F1 bag 2', inspiration='F1', price=550, image='https://i.pinimg.com/736x/9b/6b/29/9b6b29437b08336e1df60d6a1e7f2d80.jpg'),
    Bag(name='Steve Lacy bag 1', inspiration='Steve Lacy', price=550, image='https://i.pinimg.com/736x/25/09/d5/2509d5ec52ccd970a39bfd9f9ccf0c04.jpg'),
    Bag(name='Future bag 1', inspiration='Future', price=550, image='https://i.pinimg.com/736x/05/c3/a7/05c3a755b0b0a6fa24e4e01a2f5505b1.jpg'),
    Bag(name='Future bag 2', inspiration='Future', price=550, image='https://i.pinimg.com/736x/42/6f/ce/426fce351e803fd3a233428c947c3ae5.jpg'),
    Bag(name='Future bag 3', inspiration='Future', price=550, image='https://i.pinimg.com/736x/21/8e/f9/218ef95a0cf43d5055cd6fb8c75ca73c.jpg'),
    Bag(name="Daniel Caesar bag 1", inspiration='Daniel Caesar', price=550, image='https://i.pinimg.com/474x/c2/ad/88/c2ad8805786fe6164d1bfa6b66bc1883.jpg'),
    # Bags inspired by Daniel Caesar
    Bag(name="Daniel Caesar bag 2", inspiration='Daniel Caesar', price=550, image='https://i.pinimg.com/474x/48/88/6f/48886f95012fc805b55b78244470a2b3.jpg'),
    Bag(name="Daniel Caesar bag 3", inspiration='Daniel Caesar', price=550, image='https://i.pinimg.com/474x/ba/f0/31/baf0318f68cc365c1bba28840027e5a6.jpg'),
    Bag(name="Daniel Caesar bag 4", inspiration='Daniel Caesar', price=550, image='https://i.pinimg.com/474x/ca/3a/40/ca3a403e9de472451cbbb21c13a13f1d.jpg'),
    Bag(name="Daniel Caesar bag 5", inspiration='Daniel Caesar', price=550, image='https://i.pinimg.com/474x/94/ca/c6/94cac6a789f31eec0ae24f51d4726d7f.jpg'),

    # Bags inspired by Girlfriend
    Bag(name="Girlfriend bag 1", inspiration='Girlfriend', price=550, image='https://i.pinimg.com/474x/f7/10/2b/f7102b27e01a201b1a23ffdd88537f20.jpg'),
    Bag(name="Girlfriend bag 2", inspiration='Girlfriend', price=550, image='https://i.pinimg.com/474x/d7/8e/d0/d78ed09c1125894fb59cf78039e2fd50.jpg'),
    Bag(name="Girlfriend bag 3", inspiration='Girlfriend', price=550, image='https://i.pinimg.com/474x/b9/07/cd/b907cd99f64fae97dafaa26bd5f3c134.jpg'),

    # Bags inspired by Outerbanks
    Bag(name="Outerbanks bag 1", inspiration='Outerbanks', price=550, image='https://i.pinimg.com/474x/e2/61/85/e261855d5ec51b129ad1e5164a0120e3.jpg'),
    Bag(name="Outerbanks bag 2", inspiration='Outerbanks', price=550, image='https://i.pinimg.com/474x/c1/e3/a8/c1e3a8a47f989b8851407c0e6fe83c78.jpg'),
    Bag(name="Outerbanks bag 3", inspiration='Outerbanks', price=550, image='https://i.pinimg.com/474x/d7/c0/ce/d7c0ce4ee05a22326c6af29417697b46.jpg'),
    Bag(name="Outerbanks bag 4", inspiration='Outerbanks', price=550, image='https://i.pinimg.com/474x/e8/0c/8b/e80c8b9f08de0ca20b9356273c616d9e.jpg'),
    Bag(name="Outerbanks bag 5", inspiration='Outerbanks', price=550, image='https://i.pinimg.com/474x/cd/51/48/cd5148d4581fbaa39d5b90516fe9be01.jpg'),

]   
tshirts = [
    Tshirt(name="Brent Faiyaz t-shirt 1", inspiration='Brent Faiyaz', price=950, image='https://i.pinimg.com/736x/53/cf/a5/53cfa5eb6c2bb96de524c9d8d827cc06.jpg'),
    Tshirt(name="Brent Faiyaz t-shirt 2", inspiration='Brent Faiyaz', price=950, image='https://i.pinimg.com/474x/58/e7/a3/58e7a3fa71940c6dfa8c070d8b3b6735.jpg'),
    Tshirt(name="Brent Faiyaz t-shirt 3", inspiration='Brent Faiyaz', price=950, image='https://i.pinimg.com/474x/8e/68/03/8e6803a988c82cccb2dc2d726a802f2d.jpg'),
    Tshirt(name="Brent Faiyaz t-shirt 4", inspiration='Brent Faiyaz', price=950, image='https://i.pinimg.com/474x/36/fd/33/36fd33ad680c79ea7f775fbca6f6a808.jpg'),
    Tshirt(name="Brent Faiyaz t-shirt 5", inspiration='Brent Faiyaz', price=950, image='https://i.pinimg.com/474x/84/1e/d1/841ed1833b92d63db07f225d71ce25d8.jpg'),
    Tshirt(name="Brent Faiyaz t-shirt 6", inspiration='Brent Faiyaz', price=950, image='https://i.pinimg.com/474x/4a/fb/94/4afb9452c4205c2a787e656428bf852c.jpg'),
    Tshirt(name="Brent Faiyaz t-shirt 7", inspiration='Brent Faiyaz', price=950, image='https://i.pinimg.com/474x/ea/c1/59/eac1590e1b9ff1541e36f6cbeaeddafe.jpg'),
    Tshirt(name='Jcole t-shirt 1', inspiration='JCole', price=950, image='https://i.pinimg.com/736x/63/32/9c/63329ced5bd2142254cdaf6e2373351e.jpg'),
    # T-shirts inspired by Drake
    Tshirt(name="Drake t-shirt 1", inspiration='Drake', price=950, image=''),
    Tshirt(name="Drake t-shirt 2", inspiration='Drake', price=950, image=''),
    Tshirt(name="Drake t-shirt 3", inspiration='Drake', price=950, image=''),
    Tshirt(name="Drake t-shirt 4", inspiration='Drake', price=950, image=''),
    Tshirt(name="Drake t-shirt 5", inspiration='Drake', price=950, image=''),
    Tshirt(name="Drake t-shirt 6", inspiration='Drake', price=950, image=''),
    Tshirt(name="Drake t-shirt 7", inspiration='Drake', price=950, image=''),
    Tshirt(name="Drake t-shirt 8", inspiration='Drake', price=950, image=''),

    # T-shirts inspired by Kendrick Lamar
    Tshirt(name="Kendrick Lamar t-shirt 1", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 2", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 3", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 4", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 5", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 6", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 7", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 8", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 9", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 10", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 11", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 12", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 13", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 14", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 15", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 16", inspiration='Kendrick Lamar', price=950, image=''),
    Tshirt(name="Kendrick Lamar t-shirt 17", inspiration='Kendrick Lamar', price=950, image=''),

    # T-shirts inspired by F1
    Tshirt(name="F1 t-shirt 1", inspiration='F1', price=950, image='https://i.pinimg.com/736x/65/24/15/6524159e0e03354dd63a46299ecb7509.jpg'),
    Tshirt(name="F1 t-shirt 2", inspiration='F1', price=950, image='https://i.pinimg.com/736x/b2/9c/80/b29c802e704efca6598c432d5bbb9869.jpg'),
    Tshirt(name="F1 t-shirt 3", inspiration='F1', price=950, image='https://i.pinimg.com/736x/1f/62/c9/1f62c9fc7f11c735d0ce647485f92b25.jpg'),
    Tshirt(name="F1 t-shirt 4", inspiration='F1', price=950, image='https://i.pinimg.com/736x/a1/23/8e/a1238ec4c16954dc2b5ff584d20cc0f1.jpg'),
    Tshirt(name="F1 t-shirt 5", inspiration='F1', price=950, image='https://i.pinimg.com/736x/d5/a4/08/d5a4085397b88d0469c35d11a9e9e3fd.jpg'),
    Tshirt(name="F1 t-shirt 6", inspiration='F1', price=950, image='https://i.pinimg.com/736x/b2/41/bf/b241bfd3a1996958309e18f29da110c6.jpg'),
    Tshirt(name="F1 t-shirt 7", inspiration='F1', price=950, image='https://i.pinimg.com/736x/f6/ce/78/f6ce7804ad49ed24be0fdec7dc1eb7c0.jpg'),

    # T-shirts inspired by Girlfriend
    Tshirt(name="Girlfriend t-shirt 1", inspiration='Girlfriend', price=950, image=''),
    Tshirt(name="Girlfriend t-shirt 2", inspiration='Girlfriend', price=950, image=''),

    # T-shirts inspired by Outerbanks
    Tshirt(name="Outerbanks t-shirt 1", inspiration='Outerbanks', price=950, image=''),
    Tshirt(name="Outerbanks t-shirt 2", inspiration='Outerbanks', price=950, image=''),
    Tshirt(name="Outerbanks t-shirt 3", inspiration='Outerbanks', price=950, image=''),

]
with app.app_context():
    db.session.query(Bag).delete()
    db.session.query(Cap).delete()
    db.session.query(Tshirt).delete()

    db.session.add_all(bags)
    # db.session.add_all(caps)
    db.session.add_all(tshirts)
    db.session.commit()