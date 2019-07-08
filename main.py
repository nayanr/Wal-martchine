from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


import csv
import pandas as pd
import numpy as np
from numpy import array
u_i = pd.read_csv("u_i.csv")
u_i = u_i.set_index(["dish_id"])
u_i = u_i.drop(columns=['Unnamed'])
u, sig, v_transposed = np.linalg.svd(u_i, full_matrices=False)
sum_sig_90 = sum(sig)*0.9
sum_sig_90
for i in range(len(sig)):
    sum_sig_90 = sum_sig_90 - sig[i]
    if(sum_sig_90<=0):
        j = i
        break
sig_new = sig[:j]

u_refined = u[:,:j]
v_t_refined = v_transposed[:j]

u_i_SVD = np.dot(u_refined, np.dot(np.diag(sig_new), v_t_refined))

























def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = ?", (session['email'], ))
            userId, firstName = cur.fetchone()
            cur.execute("SELECT count(productId) FROM kart WHERE userId = ?", (userId, ))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn,firstName, noOfItems)

@app.route("/")
def root():
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price FROM products')
        itemData = cur.fetchall()
    itemData = parse(itemData)   
    return render_template('home.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/add")
def admin():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        
    conn.close()
    return render_template('add.html')

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        name = request.form['name']
        price = float(request.form['price'])
        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO products (name, price) VALUES (?, ?)''', (name, price))
                conn.commit()
                msg="added successfully"
            except:
                msg="error occured"
                conn.rollback()
        conn.close()
        print(msg)
        return redirect(url_for('root'))

@app.route("/add_directly", methods=["GET", "POST"])
def add_directly():
    
#    import pandas as pd
#    df = pd.read_csv("filtered.csv")
#    
#    
#    ingredientlist = []
#    for i,row in df.iterrows():
#        list_1 = row['ingredients']
#        print(list_1)
#        for item in list_1:
#            
#            if(item in ingredientlist):
#                continue
#            else:
#                
#                ingredientlist.append(item)
    ingredientlist = ['romaine lettuce', 'black olives', 'grape tomatoes', 'garlic', 'pepper', 'purple onion', 'seasoning', 'garbanzo beans', 'feta cheese crumbles', 'water', 'vegetable oil', 'wheat', 'salt', 'black pepper', 'shallots', 'cornflour', 'cayenne pepper', 'onions', 'garlic paste', 'milk', 'butter', 'lemon juice', 'chili powder', 'passata', 'oil', 'ground cumin', 'boneless chicken skinless thigh', 'garam masala', 'double cream', 'natural yogurt', 'bay leaf', 'plain flour', 'sugar', 'eggs', 'fresh ginger root', 'ground cinnamon', 'vanilla extract', 'ground ginger', 'powdered sugar', 'baking powder', 'olive oil', 'medium shrimp', 'chopped cilantro', 'jalapeno chilies', 'flat leaf parsley', 'skirt steak', 'white vinegar', 'sea salt', 'chorizo sausage', 'pistachio nuts', 'white almond bark', 'flour', 'almond extract', 'dried cranberries', 'fresh pineapple', 'pork', 'poblano peppers', 'corn tortillas', 'cheddar cheese', 'ground black pepper', 'iceberg lettuce', 'lime', 'chopped cilantro fresh', 'chopped tomatoes', 'fresh basil', 'extra-virgin olive oil', 'kosher salt', 'pimentos', 'sweet pepper', 'dried oregano', 'sharp cheddar cheese', 'swiss cheese', 'provolone cheese', 'canola oil', 'mushrooms', 'sausages', 'low sodium soy sauce', 'fresh ginger', 'dry mustard', 'green beans', 'white pepper', 'sesame oil', 'scallions', 'Shaoxing wine', 'ground turkey', 'crushed red pepper flakes', 'corn starch', 'Italian parsley leaves', 'walnuts', 'hot red pepper flakes', 'fresh lemon juice', 'trout fillet', 'garlic cloves', 'chipotle chile', 'fine sea salt', 'fresh cilantro', 'ground coriander', 'plum tomatoes', 'avocado', 'lime juice', 'flank steak', 'fresh parmesan cheese', 'all-purpose flour', 'fat free less sodium chicken broth', 'chopped fresh chives', 'gruyere cheese', 'bacon slices', 'gnocchi', 'fat free milk', 'cooking spray', 'tumeric', 'vegetable stock', 'tomatoes', 'naan', 'red lentils', 'red chili peppers', 'spinach', 'sweet potatoes', 'greek yogurt', 'lemon curd', 'confectioners sugar', 'raspberries', 'italian seasoning', 'broiler-fryer chicken', 'mayonaise', 'zesty italian dressing', 'roma tomatoes', 'sesame seeds', 'red pepper', 'yellow peppers', 'extra firm tofu', 'broccoli', 'soy sauce', 'orange bell pepper', 'arrowroot powder', 'red curry paste', 'marinara sauce', 'linguine', 'capers', 'olives', 'lemon zest', 'lo mein noodles', 'chicken broth', 'light soy sauce', 'beansprouts', 'dried black mushrooms', 'chives', 'oyster sauce', 'dark soy sauce', 'peanuts', 'cabbage', 'sliced mushrooms', 'sherry', 'grated parmesan cheese', 'heavy cream', 'spaghetti', 'cooked chicken', 'green bell pepper', 'egg roll wrappers', 'sweet and sour sauce', 'molasses', 'shredded cabbage', 'ground pork', 'carrots', 'flour tortillas', 'cheese', 'breakfast sausages', 'large eggs', 'yellow corn meal', 'boiling water', 'garlic powder', 'onion powder', 'paprika', 'crushed garlic', 'green onions', 'white sugar', 'dried basil', 'diced tomatoes', 'bread slices', 'great northern beans', 'shrimp', 'sage leaves', 'Oscar Mayer Deli Fresh Smoked Ham', 'hoagie rolls', 'salami', 'giardiniera', 'mozzarella cheese', 'pepperoni', 'enchilada sauce', 'sliced green onions', 'picante sauce', 'green pepper', 'canned black beans', 'shredded lettuce', 'sour cream', 'shredded cheddar cheese', 'salmon fillets', 'cumin seed', 'curry powder', 'serrano chile', 'sauce', 'chicken breast halves', 'lettuce leaves', 'chopped onion', 'mandarin oranges', 'orange liqueur', 'yellow cake mix', 'frosting', 'bay leaves', 'crushed red pepper', 'mussels', 'basil', 'dry white wine', 'finely chopped onion', 'lemon', 'pesto', 'white wine', 'bread crumbs', 'unsalted butter', 'curry', 'low sodium beef broth', 'pickapeppa sauce', 'cold water', 'yellow onion', 'allspice', 'fresh thyme', 'worcestershire sauce', 'ground beef', 'coarse salt', 'fenugreek', 'urad dal', 'potatoes', 'white rice', 'pizza crust', 'part-skim mozzarella cheese', 'chicken legs', 'chile pepper', 'ghee', 'tomato paste', 'ground turmeric', 'stock', 'cracked black pepper', 'minced beef', 'celery', 'dried thyme', 'ginger', 'chillies', 'crushed tomatoes', 'fresh rosemary', 'boneless pork loin', 'pappardelle', 'jasmine rice', 'shiitake', 'Gochujang base', 'top round steak', 'rice vinegar', 'Taiwanese bok choy', 'serrano ham', 'manchego cheese', 'dijon mustard', 'sourdough', 'membrillo', 'burger buns', 'panko breadcrumbs', 'chickpea flour', 'Sriracha', 'chickpeas', 'ground flaxseed', 'greens', 'tahini', 'Italian bread', 'balsamic vinegar', 'sausage casings', 'honey', 'shredded mozzarella cheese', 'roasted red peppers', 'penne pasta', 'green chilies', 'fenugreek leaves', 'black mustard seeds', 'amchur', 'lime wedges', 'coriander', 'fingerling potatoes', 'ramps', 'black peppercorns', 'cinnamon sticks', 'cardamom pods', 'coriander seeds', 'asiago', 'whole wheat pasta', 'sweet onion', 'chestnuts', 'granulated sugar', 'whole milk ricotta cheese', 'coffee ice cream', 'mascarpone', 'rum', 'semisweet chocolate', 'chestnut flour', 'baby spinach leaves', 'chopped garlic', 'large shrimp', 'barley', 'cooked ham', 'red bell pepper', 'bacon', 'starchy potatoes', 'grated nutmeg', 'finely chopped fresh parsley', 'vinegar', 'caul fat', 'whole milk', 'golden brown sugar', 'heavy whipping cream', 'kahlÃºa', 'instant espresso powder', 'epazote', 'radishes', 'oregano', 'white onion', 'hominy', 'tomatillos', 'pepitas', 'coconut milk', 'basmati rice', 'cauliflower', 'cumin', 'blood orange', 'freshly ground pepper', 'fennel bulb', 'low salt chicken broth', 'white wine vinegar', 'tomato sauce', 'shredded carrots', 'english muffins, split and toasted', 'vegetable oil cooking spray', 'chopped green bell pepper', 'lasagna noodles', 'ranch dressing', 'evaporated milk', 'minced garlic', 'red wine vinegar', 'boneless chop pork', 'chile paste', 'fresh lime juice', 'lower sodium soy sauce', 'dark sesame oil', 'raisins', 'pearl barley', 'slivered almonds', 'chocolate bars', 'marshmallows', 'cinnamon graham crackers', 'noodles', 'baby bok choy', 'black bean sauce', 'red potato', 'chinese rice wine', 'cooking oil', 'black beans', 'quinoa', 'frozen corn', 'vegetable broth', 'orange', 'star anise', 'chinese five-spice powder', 'brown sugar', 'duck', 'napa cabbage leaves', 'chicken leg quarters', 'cucumber', 'long-grain rice', 'piloncillo', 'ground allspice', 'hibiscus', 'ground cloves', 'ground nutmeg', 'fresh parsley', 'fresh oregano', 'chocolate morsels', 'cream sweeten whip', 'instant espresso granules', 'whipping cream', 'chocolate covered coffee beans', 'unflavored gelatin', 'pound cake', 'pinenuts', 'zucchini', 'baby carrots', 'fresh basil leaves', 'asparagus spears', 'frozen peas', 'arborio rice', 'yellow crookneck squash', 'chipotles in adobo', 'instant white rice', 'cilantro leaves', 'red beans', 'chopped celery', 'skinless chicken thighs', 'lime zest', 'condensed cream of mushroom soup', 'condensed cream of chicken soup', 'lean ground beef', 'Mexican cheese blend', 'chunky salsa', 'taco seasoning mix', 'chorizo spanish', 'pineapple juice', 'dark rum', 'daikon', 'pork ribs', 'goji berries', 'oysters', 'salsa', 'demerara sugar', 'egg whites', 'fruit', 'dried currants', 'frozen pastry puff sheets', 'mixed spice', 'parsnips', 'chili oil', 'brown mustard seeds', 'yukon gold potatoes', 'refried beans', 'grated jack cheese', 'hot sauce', 'egg yolks', 'fresh leav spinach', 'cheese tortellini', 'cherry tomatoes', 'navy beans', 'nonfat milk', 'granny smith apples', 'chicken breasts', 'lard', 'golden raisins', 'yellow bell pepper', 'ground pepper', 'pecorino romano cheese', 'fresh fava bean', 'italian sausage', 'large garlic cloves', 'pasta sheets', 'fish sauce', 'spinach leaves', 'low-fat natural yogurt', 'Flora Cuisine', 'curry paste', 'chicken stock', 'bone-in chicken breasts', 'white hominy', 'tortilla chips', 'dried chile peppers', 'large egg whites', 'moong dal', 'capsicum', 'green mango', 'mirin', 'toasted sesame oil', 'tofu', 'short-grain rice', 'dried shiitake mushrooms', 'gari', 'Turkish bay leaves', 'dried chickpeas', 'celery ribs', 'semolina', 'warm water', 'vine ripened tomatoes', 'bittersweet chocolate', 'fat free yogurt', 'skim milk', 'angel food cake', 'unsweetened cocoa powder', 'instant espresso', 'anise', 'zinfandel', 'orange blossom honey', 'calimyrna figs', 'clove', 'plain whole-milk yogurt', 'garlic salt', 'chili paste', 'red pepper flakes', 'kiwi', 'asian pear', 'chees fresco queso', 'swiss chard', 'prawns', 'veal cutlets', 'pasta', 'wakame', 'extra-lean ground beef', 'scallion greens', 'wonton wrappers', 'peeled fresh ginger', 'nonstick spray', 'coconut oil', 'ground red pepper', 'almond flour', 'coconut aminos', 'saffron', 'green peas', 'clams', 'boneless skinless chicken breast halves', 'seasoned rice wine vinegar', 'snow peas', 'hard-boiled egg', 'artichoke hearts', 'pita bread rounds', 'eggplant', 'whole peeled tomatoes', 'shredded Monterey Jack cheese', 'pickled jalapenos', 'broccoli rabe', 'parmigiano reggiano cheese', 'dry bread crumbs', 'fontina', 'pasta sauce', 'olive oil flavored cooking spray', 'frozen chopped spinach', 'part-skim ricotta cheese', 'manicotti shells', 'fettucine', 'parmesan cheese', 'chicken bouillon', 'peanut oil', 'chili paste with garlic', 'fresh veget', 'taco sauce', 'guacamole', 'salsa verde', 'condiments', 'pork shoulder roast', 'tortillas', 'rose petals', 'almonds', 'rice', 'pistachios', 'chicken wings', 'drumstick', 'green chile', 'peeled tomatoes', 'chicken', 'chiles', 'adobo sauce', 'ancho powder', 'chipotle chile powder', 'Old El Paso Flour Tortillas', 'cranberry sauce', 'beer', 'chili sauce', 'beef rib short', 'fresh dill', 'yoghurt', 'myzithra', 'feta cheese', 'phyllo', 'kefalotyri', 'black-eyed peas', 'Philadelphia Cream Cheese', 'crab meat', 'savoy cabbage', 'baking potatoes', 'cream of tartar', 'semi-sweet chocolate morsels', 'cake flour', 'ricotta cheese', 'cream cheese', 'serrano', 'hamburger buns', 'chopped fresh mint', 'ground lamb', 'dried porcini mushrooms', 'chopped fresh thyme', 'dry red wine', 'hot water', 'fat free less sodium beef broth', 'cremini mushrooms', 'pitted kalamata olives', 'strong white bread flour', 'salted butter', 'sunflower oil', 'kalonji', 'instant yeast', 'fresh coriander', 'cooked white rice', 'mixed mushrooms', 'wood ear mushrooms', 'vegetables', 'taco seasoning', 'bell pepper', 'boneless skinless chicken breasts', 'shredded cheese', 'salt and ground black pepper', 'sliced black olives', 'chopped green chilies', 'water chestnuts, drained and chopped', 'chinese cabbage', 'dipping sauces', 'lean ground pork', 'pico de gallo', 'cheese slices', 'chorizo', 'french bread', 'dried mint flakes', 'dried dillweed', 'red wine', 'lamb', 'plain yogurt', 'kale', 'Mexican beer', 'boneless beef short ribs', 'guajillo', 'saffron threads', 'fresh spinach', 'dry sherry', 'banana squash', 'cannellini beans', 'Franks Hot Sauce', 'cooked rice', 'cilantro', 'skinless chicken breasts', 'light sour cream', 'fava beans', 'fresh tarragon', 'kidney beans', 'whole kernel corn, drain', 'orzo pasta', 'grated lemon zest', 'chopped almonds', 'baby arugula', 'tequila', 'margarita mix', 'self rising flour', 'apple cider vinegar', 'jamaican jerk season', 'pineapple preserves', 'chicken drumsticks', 'pitas', 'goat cheese', 'gingerroot', 'rib eye steaks', 'hot bean paste', 'medjool date', 'diced bell pepper', 'cream', 'smoked paprika', 'reduced fat milk', 'smoked trout', 'asparagus', 'garlic puree', 'green cardamom pods', 'tomato purÃ©e', 'pickled jalapeno peppers', 'romaine lettuce leaves', 'crema mexicana', 'corn oil', 'chile sauce', 'chicken thighs', 'queso fresco', 'reduced sodium soy sauce', 'Korean chile flakes', 'red chile powder', 'boneless chicken breast', 'cashew nuts', 'mace', 'kashmiri chile', 'kasuri methi', 'mustard oil', 'ginger paste', 'cinnamon', 'tomato ketchup', 'tostada shells', 'grouper', 'low-fat sour cream', 'corn kernels', 'ricotta salata', 'pecorino cheese', 'grana padano', 'ketchup', 'liquid', 'jeera', 'cardamom', 'monterey jack', 'crema', 'buttermilk', 'jam', 'baking soda', 'shredded sharp cheddar cheese', 'dinner rolls', 'cactus pad', 'fenugreek seeds', 'cauliflower flowerets', 'boiling potatoes', 'fennel seeds', 'baby spinach', 'tuna steaks', 'spices', 'octopuses', 'vidalia onion', 'smoked gouda', 'small red potato', 'tuna', 'fat-free refried beans', 'low-fat milk', 'fresh lime', 'whiskey', 'hoisin sauce', 'BertolliÂ® Classico Olive Oil', 'bacon, crisp-cooked and crumbled', 'bertolli vineyard premium collect marinara with burgundi wine sauc', 'bread crumb fresh', 'margarita salt', '(    oz.) tomato sauce', 'ground veal', 'italian seasoning mix', 'beef', 'fat skimmed chicken broth', 'solid pack pumpkin', 'fresh thyme leaves', 'whole grain thin spaghetti', 'grapeseed oil', 'organic sugar', 'dried cherry', 'prosciutto', 'romano cheese', 'cooked shrimp', 'crabmeat', 'vegan margarine', 'parsley leaves', 'fresh raspberries', 'frozen whole kernel corn', 'wish bone guacamol ranch dress', 'torn romain lettuc leav', 'russet potatoes', 'mexican chorizo', 'colby cheese', 'half & half', 'dry vermouth', 'canned low sodium chicken broth', 'chicken livers', 'roasted salted cashews', 'fresh lemon', 'toasted sesame seeds', 'paneer cheese', 'low sodium chicken broth', 'boneless center cut pork chops', 'pork tenderloin', 'steamed white rice', 'caramel sauce', 'chili pepper', 'boneless skinless chicken', 'seasoned bread crumbs', 'bean threads', 'safflower oil', 'cayenne', 'reduced sodium tamari', 'liquorice', 'green cardamom', 'szechwan peppercorns', 'chinese black bean', 'cooking wine', 'dried chile', 'rock sugar', 'bean paste', 'brown cardamom', 'leg of lamb', 'parsley', 'red kidney beans', 'coriander powder', 'fillets', 'spring onions', 'bamboo shoots', 'fresh mushrooms', 'red radishes', 'chili flakes', 'napa cabbage', 'granulated garlic', 'beans', 'jack cheese', 'ricotta', 'reduced sodium chicken broth', 'mung bean sprouts', 'sesame paste', 'pickled vegetables', 'jaggery', 'ground cardamom', 'coconut', 'rice flour', 'spam', 'rice cakes', 'firm tofu', 'kimchi', 'chili', 'cider vinegar', 'fresh mint', 'polenta', 'olive oil cooking spray', 'cauliflower florets', 'sweet chili sauce', 'maida flour', 'Old El Pasoâ„¢ mild red enchilada sauce', 'Pillsburyâ„¢ Refrigerated Crescent Dinner Rolls', 'refrigerated crescent rolls', 'red enchilada sauce', 'jumbo shrimp', 'sea scallops', 'grate lime peel', 'bottled clam juice', 'sun-dried tomatoes in oil', 'unsalted dry roast peanuts', 'dried red chile peppers', 'cooked brown rice', 'bok choy', 'salted roast peanuts', 'onion tops', 'masa harina', 'duck breast halves', 'mint leaves', 'sliced almonds', 'vanilla lowfat yogurt', 'pesto sauce', 'arugula', 'active dry yeast', 'cream cheese, soften', 'coconut sugar', 'white corn tortillas', 'plantains', 'summer squash', 'ciabatta', 'juice', 'fresh herbs', 'grated lemon peel', 'plum sauce', 'dough', 'coarse sea salt', 'rosemary leaves', 'brie cheese', 'cheese ravioli', 'Italian seasoned breadcrumbs', 'slaw mix', 'chunky peanut butter', 'pickles', 'hoagie buns', 'fat-free cottage cheese', 'oven-ready lasagna noodles', 'margarine', 'radicchio', 'sweet paprika', 'andouille sausage links', 'rubbed sage', 'dried rosemary', 'canned beef broth', 'kale leaves', 'chicken noodle soup', 'italian style rolls', 'genoa salami', 'boiled ham', 'capicola', 'fresh tomatoes', 'table cream', 'grating cheese', 'english cucumber', 'dill', 'quail', 'lemongrass', 'diced celery', 'italian salad dressing mix', 'round steaks', 'carbonated beverages', 'saltines', 'barbecue sauce', 'prepared pizza crust', 'SargentoÂ® Traditional Cut Shredded Mozzarella Cheese', 'ice water', 'asparagus tips', 'nutmeg', 'fresh chives', 'artichokes', 'portabello mushroom', 'medium eggs', 'watercress', 'allspice berries', 'tomatillo salsa', 'pork shoulder', 'store bought low sodium chicken stock', 'chipotle', 'ground chicken', 'tamarind pulp', 'coconut cream', 'mustard seeds', 'plain breadcrumbs', 'large egg yolks', 'back bacon rashers', 'uncook medium shrimp, peel and devein', 'catfish', 'basil pesto sauce', 'aioli', 'mozzarella balls', 'sun-dried tomatoes', 'pasilla pepper', 'corn', 'Mexican cheese', 'roasted tomatoes', 'corn chips', 'chinese noodles', 'ground white pepper', 'fettuccine pasta', 'lager beer', 'poblano chiles', 'vinaigrette dressing', 'kalamata', 'turbinado', 'chicken fingers', 'hot pepper sauce', 'apricot preserves', 'ginger juice', 'sesame salt', 'rice wine', 'frozen spinach', 'lasagne', 'fat free cream cheese', 'non-fat sour cream', 'reduced fat swiss cheese', 'fat-free mayonnaise', 'roasted garlic', 'sundried tomato paste', 'porcini', 'sourdough loaf', 'crust', 'duck fat', 'squabs', 'confit', 'diced onions', 'canned corn', 'lettuce', 'aged gouda', 'soppressata', 'chopped parsley', 'couscous', 'anchovy fillets', 'lemon slices', 'chicken cutlets', 'corn flour', 'wheat flour', 'orzo', 'veal chops', 'coarse kosher salt', 'ancho chile pepper', 'masa', 'oil cured olives', 'pasta rotel', 'pasta water', 'tamarind', 'black salt', 'crusty bread', 'uncooked rigatoni', 'long grain white rice', 'cornmeal', 'fish fillets', 'old bay seasoning', 'green bell pepper, slice', 'red chili powder', 'rolls', 'cinnamon sugar', 'vanilla', 'pepper flakes', 'pears', 'rice syrup', 'corn syrup', 'bosc pears', 'buckwheat noodles', 'mustard powder', 'curry leaves', 'freshly grated parmesan', 'hass avocado', 'pitted olives', 'florets', 'thyme sprigs', 'short rib', 'sambal ulek', 'steamed rice', 'penne', 'mint', 'berries', 'melted butter', 'figs', 'graham cracker crumbs', 'sprinkles', 'Oscar Mayer Bacon', "Campbell's Condensed Tomato Soup", 'pork belly', 'mustard', 'minced ginger', 'brussels sprouts', 'crumbled gorgonzola', 'blanched almond flour', 'tapioca flour', 'mild olive oil', 'fontina cheese', 'lamb shanks', 'rosemary sprigs', 'greek seasoning', 'brown rice', 'fresh mexican cheese', "Hellmann''s Light Mayonnaise", 'crumbs', 'chipotle salsa', 'refrigerated buttermilk biscuits', 'peeled shrimp', 'ground thyme', 'malt vinegar', 'pork butt', 'crÃ¨me fraÃ®che', 'chutney', 'canned chicken breast', 'italian eggplant', 'Sicilian olives', 'mint sprigs', 'peasant bread', 'ziti', 'tandoori spices', 'methi', 'curds', 'Kraft Grated Parmesan Cheese', 'peas', 'brown lentils', 'dried minced onion', 'orange juice', 'sliced ham', 'butternut squash', 'garnish', 'dried navy beans', 'wheat berries', 'parsley sprigs', 'thyme', 'polenta prepar', 'hash brown', 'stewed tomatoes', 'cocoa powder', 'dried parsley', 'bananas', 'peaches', 'asafoetida powder', 'ravva', 'water chestnuts', 'chinese hot mustard', 'steamer', 'soy marinade', 'fish', 'asafetida', 'rigatoni', 'pancetta', 'whole wheat fettuccine', 'ground sirloin', 'fresh marjoram', 'castellane', 'hot Italian sausages', 'french rolls', 'jumbo pasta shells', 'gluten free blend', 'bone in skinless chicken thigh', 'Mexican seasoning mix', 'light cream cheese', 'egg substitute', 'mini chocolate chips', 'mini marshmallows', 'peanut butter', 'ham', 'balsamic vinaigrette', 'pepper sauce', 'greek style plain yogurt', 'asadero', 'mild curry powder', 'beef stew', 'pickling spices', 'teriyaki sauce', 'petite peas', 'chicken meat', 'puff pastry', 'flour for dusting', 'white mushrooms', 'haricots verts', 'fresh peas', 'bow-tie pasta', 'seedless green grape', 'country white bread', 'flaked coconut', 'leaf parsley', 'chipotle peppers', 'pinto beans', 'fresh tomato salsa', 'Greek feta', 'pitted prunes', 'medium egg noodles', 'stir fry vegetable blend', 'Madras curry powder', 'low-fat cottage cheese', 'whole wheat lasagna noodles', 'shredded parmesan cheese', 'frozen corn kernels', 'spring mix', 'burgers', 'fresh green bean', 'apricots', 'grappa', 'beef tenderloin', 'marinade', 'sirloin tip', 'whole wheat tortillas', 'nutritional yeast', 'low-fat soy milk', 'marmite', 'bagels', 'superfine sugar', 'chicken bouillon granules', 'all purpose unbleached flour', 'dry yeast', 'amaretti', 'frozen strawberries', 'strawberries', 'Tabasco Pepper Sauce', 'fino sherry', 'Alfredo sauce', 'chopped fresh sage', 'beef brisket', 'jack', 'Hatch Green Chiles', 'bread', 'morel', 'leeks', 'red bell pepper, sliced', 'snappers', '1% low-fat cottage cheese', 'fresh sage', 'pork loin', 'cotija', 'green cabbage', 'dry coconut', 'diced green chilies', 'chili beans', 'tenderloin', 'rotisserie chicken', 'udon', 'orange zest', 'broccoli florets', 'veggies', 'parmigiano-reggiano cheese', 'baguette', 'roasted peanuts', 'gluten free soy sauce', 'toasted walnuts', 'lower sodium chicken broth', 'acorn squash', 'white beans', 'lamb chops', 'romana', 'seafood stock', 'steak', 'white cheddar cheese', 'crystallized ginger', 'pecan halves', 'mandarin orange segments', 'dressing', 'dark brown sugar', 'dark molasses', 'scotch bonnet chile', 'okra', 'bone in chicken thighs', 'light coconut milk', 'canned chopped tomatoes', 'crimini mushrooms', 'navel oranges', 'serrano peppers', 'meat', 'lean ground turkey', 'white bread', 'pork loin chops', 'sake', 'ladyfingers', 'reduced fat cream cheese', 'whipped topping', 'unsweetened chocolate', 'sticky rice', 'chile bean paste', 'homemade chicken stock', 'hot curry powder', 'Hurst Family Harvest Chipotle Lime Black Bean Soup mix', 'gluten free cooking spray', 'gluten free corn tortillas', 'chipotle puree', 'wine', 'Mexican oregano', 'cottage cheese', 'tahini paste', 'green olives', 'caster', 'salad leaves', 'scallops', 'garden peas', 'maldon sea salt', 'bacon rind', 'runny honey', 'frozen broccoli', 'fresh curry leaves', 'chuck', 'dill weed', 'nonfat ricotta cheese', 'pork baby back ribs', 'spiced rum', 'jerk seasoning', 'bbq sauce', 'chile powder', 'mexican chocolate', 'shells', 'reduced-fat cheese', 'cornflake cereal', 'basil leaves', 'frozen orange juice concentrate', 'cherries', 'achiote paste', 'poblano chilies', 'fresh lima beans', 'cilantro sprigs', 'crusty sandwich rolls', 'tilapia fillets', 'dry pasta', 'sweet italian sausage', 'oyster mushrooms', 'sirloin', 'apples', 'firmly packed brown sugar', 'fat', 'fat-trimmed beef flank steak', 'salad oil', 'prosecco', 'bread dough', 'cooked turkey', 'leftover gravy', 'mashed potatoes', 'turkey broth', 'stuffing', 'baby lima beans', 'fresca', 'relish', 'slaw', 'whipped cream', 'hot cocoa mix', 'brewed coffee', 'abbamele', 'wild mushrooms', 'chopped walnuts', 'fregola', 'mushroom caps', 'pinot grigio', 'liquid egg substitute', 'chocolate candy bars', 'egg noodles', 'msg', 'gai lan', 'fresh chile', 'lite coconut milk', 'pitted date', 'golden syrup', 'self-rising cake flour', 'pigeon peas', 'paneer', 'gram flour', 'soda', 'chaat masala', 'whole snapper', 'button mushrooms', 'banana peppers', 'dried fig', 'boneless beef roast', 'beef broth', 'pasilla chiles', 'pumpkin seeds', 'anise seed', 'seeds', 'chicken pieces', 'mulato chiles', "soft goat's cheese", 'truffle oil', 'hazelnuts', 'veal scallopini', 'poppy seeds', 'blanched almonds', 'raw cashews', 'gluten free all purpose flour', 'tapioca starch', 'xanthan gum', 'elbow macaroni', 'bread flour', 'bread yeast', 'vegan parmesan cheese', 'ahi', 'whole cranberry sauce', 'lotus roots', 'ginger root', 'taco shells', 'colby jack cheese', 'unsalted cashews', 'anjou pears', 'vegetable shortening', 'whole wheat flour', 'yardlong beans', 'sausage links', 'pork chops', "Campbell's Condensed Cream of Chicken Soup", 'Pace Picante Sauce', 'rosemary', 'nectarines', 'sweet cherries', 'lavender buds', 'apricot halves', 'diced tomatoes in juice', 'stewing beef', 'string beans', 'italian salad dressing', 'short pasta', 'lemon wedge', 'porterhouse steaks', 'mango', 'gooseberries', '1% low-fat milk', 'taco toppings', 'rotel tomatoes', 'flat iron steaks', 'broccolini', 'tripe', 'coffee granules', 'lemon rind', 'baby portobello mushrooms', 'dried pinto beans', 'ground chipotle chile pepper', 'blue corn tortilla chips', 'veget soup mix', 'pork lard', 'whole almonds', 'chicken bones', 'ground paprika', 'ground almonds', 'orecchiette', 'pepper jack', 'bibb lettuce', 'peeled deveined shrimp', 'bird chile', 'tiger prawn', 'and fat free half half', 'condensed chicken broth', 'pumpkin purÃ©e', 'unsalted chicken stock', 'extra lean ground beef', 'glace cherries', 'raspberry jam', 'silver dragees', 'biscuits', 'caster sugar', 'frozen raspberries', 'sponge cake', 'sweet sherry', 'vanilla pods', 'pizza shells', 'frozen mixed thawed vegetables,', 'ragu old world style pasta sauc', 'loosely packed fresh basil leaves', 'whole wheat spaghetti', 'triple sec', 'pear tomatoes', 'gaeta olives', 'turbot', 'medium-grain rice', 'fresh oregano leaves', 'refrigerated pizza dough', 'potato gnocchi', 'olive oil spray', 'lime rind', 'apple juice', 'pimenton', 'light brown sugar', 'guajillo chiles', 'sweetener', 'hibiscus tea', 'teas', 'agave nectar', 'seltzer water', 'bitters', 'angel hair', 'ground tumeric', 'whole cloves', 'red food coloring', 'shanghai noodles', 'black vinegar', 'reduced-fat sour cream', 'baked tortilla chips', 'reduced fat sharp cheddar cheese', 'gelato', 'cherry preserves', 'amaretto liqueur', 'plain low-fat yogurt', 'extra sharp cheddar cheese', 'aleppo pepper', 'nuts', 'pie shell', 'light corn syrup', 'toasted almonds', 'marsala wine', 'yellow mustard', 'applesauce', 'seasoning salt', 'cake', 'yellow food coloring', 'halibut fillets', 'lamb shoulder', 'tomatoes with juice', 'bulgur', 'fresh orange juice', 'cantaloupe', 'honeydew melon', 'confit duck leg', 'chopped fresh herbs', 'escarole', 'all beef hot dogs', 'hot dog bun', 'unsweetened coconut milk', 'sole fillet', 'serrano chilies', 'fresh onion', 'mushroom soy sauce', 'yellow rock sugar', 'spanish paprika', 'thick-cut bacon', 'prepar salsa', 'broth', 'dhal', 'yellow lentils', 'chopped pecans', 'coffee liqueur', 'daal', 'idli', 'Maggi', 'flat anchovy', 'italian loaf', 'minced onion', 'salad dressing', 'pitted black olives', 'rotini', 'frozen mixed vegetables', 'rolled oats', 'vine tomatoes', 'spanish rice', 'smoked sausage', 'canned tomatoes', 'vietnamese fish sauce', 'pork spareribs', 'chinese red vinegar', 'thai basil', 'rib', 'besan (flour)', 'bhindi', 'pastry dough', 'sage', 'cooked bacon', 'garlic chili sauce', 'dried mushrooms', 'top sirloin', 'Chinese egg noodles', 'candy', 'angel food cake mix', 'buttercream frosting', 'won ton wrappers', 'shiitake mushroom caps', 'spring greens', 'beef rump steaks', 'chestnut mushrooms', 'slab bacon', 'pig feet', 'pork bones', 'bulgur wheat', 'espresso powder', 'watermelon', 'buns', 'tandoori paste', 'boneless, skinless chicken breast', 'salad', 'risotto', 'ice cubes', 'cooked vermicelli', 'ground chicken breast', 'nonfat greek yogurt', 'shredded reduced fat cheddar cheese', 'fat-free chicken broth', 'boneless chicken thighs', 'unsalted roasted peanuts', 'galangal', 'sherry vinegar', 'dried lentils', 'free range egg', 'phyllo dough', '(10 oz.) frozen chopped spinach, thawed and squeezed dry', 'sliced shallots', 'california avocado', 'masa dough', 'corn husks', 'tzatziki', 'pita bread', 'boneless lamb', 'grapefruit', 'habanero pepper', 'grated romano cheese', 'andouille sausage', 'pimento stuffed green olives', 'littleneck clams', 'frozen sweet corn', 'whole wheat bread', 'light mayonnaise', 'salad seasoning mix', 'chili pepper flakes', 'pappardelle pasta', 'dulce de leche', 'pure vanilla extract', 'fresh mozzarella', 'stilton', 'regular soy sauce', 'chinese sausage', 'glutinous rice', 'fermented black beans', 'cream of chicken soup', 'ice', 'brandy', 'shredded zucchini', 'dried pasta', 'perilla', 'sweet rice flour', 'diced tomatoes with garlic and onion', 'ground round', 'fettuccine, cook and drain', 'low-fat buttermilk', 'unsweetened soymilk', 'cooked pumpkin', 'frozen limeade', 'lemon-lime soda', 'ditalini pasta', 'lobster', 'asian fish sauce', 'anise extract', 'mexican style 4 cheese blend', 'cheese spread', 'vegetarian refried beans', 'quinces', 'ragu old world style tradit pasta sauc', 'center cut loin pork chop', 'red cabbage', 'pancake mix', 'thai chile', 'white sesame seeds', 'store bought low sodium chicken broth', 'ground chile', 'chili bean sauce', 'beef shank', 'nonfat sweetened condensed milk', '2% reduced-fat milk', 'mahimahi', 'buffalo sauce', 'blue cheese dressing', 'cannelloni shells', 'butter cooking spray', 'light alfredo sauce', 'chees fresh mozzarella', 'red capsicum', 'sprouts', 'herbes de provence', 'fresh bay leaves', 'top sirloin steak', 'sourdough baguette', 'clams, well scrub', 'clam juice', 'pork roast', 'shrimp tails', 'bay scallops', 'lump crab meat', 'fish stock', 'capellini', 'mild curry paste', 'baby potatoes', 'fritos', 'white corn', 'ranch salad dressing mix', 'veal', 'beef stock', 'chard', 'grated GruyÃ¨re cheese', 'gold potatoes', 'pomegranate seeds', 'crushed ice', 'pomegranate juice', 'lime slices', 'panko', 'coarse-grain salt', 'hungarian sweet paprika', 'roasted hazelnuts', 'country bread', 'condensed fiesta nacho cheese soup', 'frozen tater tots', 'white cornmeal', 'Progresso Black Beans', 'green enchilada sauce', 'Old El Pasoâ„¢ chopped green chiles', 'nonfat yogurt', 'butter beans', 'pumpkin', 'Country CrockÂ® Spread', "hellmann' or best food real mayonnais", 'cactus leaf', 'chili seasoning mix', 'frisee', 'Wish-Bone Italian Dressing', 'bacon fat', 'herbs', 'pernod', 'evaporated skim milk', 'knorr garlic minicub', 'boneless pork shoulder', 'corn tortilla chips', 'ajwain', 'flat cut', 'anchovies', 'Splenda Brown Sugar Blend', 'Anaheim chile', 'liqueur', 'aged balsamic vinegar', 'rice paper', 'Mexican vanilla extract', 'low sodium vegetable broth', 'limoncello', 'prime rib', 'hot chili powder', 'golden beets', 'pizza doughs', 'black cod', 'biscuit mix', 'tamarind extract', 'sweetened condensed milk', 'KnorrÂ® Beef Bouillon', 'cavolo nero', 'winter squash', 'thin pizza crust', 'toasted pine nuts', 'red kidnei beans, rins and drain', 'beef stock cubes', 'lean beef', 'grated parmesan romano', 'fleur de sel', 'garden cress', 'mixed greens', 'kirby cucumbers', 'turkey breast cutlets', 'atta', 'methi leaves', 'pudding', 'whole wheat pastry flour', 'Neapolitan ice cream', 'boneless chicken', 'mackerel fillets', 'gluten', 'cod fillets', 'barilla', 'tomato juice', 'cooked chicken breasts', 'linguini', 'artichok heart marin', 'instant rice', 'beefsteak tomatoes', 'perciatelli', 'crumbled blue cheese', 'black mission figs']
    
    for item in ingredientlist:
        name = item
        price = float(100)
        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO products (name, price) VALUES (?, ?)''', (name, price))
                conn.commit()
                msg="added successfully"
                print(msg)
            except:
                msg="error occured"
                conn.rollback()
        conn.close()
        print(msg)
    return redirect(url_for('root'))




    


@app.route("/remove")
def remove():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price FROM products')
        data = cur.fetchall()
    conn.close()
    return render_template('remove.html', data=data)

@app.route("/removeItem")
def removeItem():
    productId = request.args.get('productId')
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM products WHERE productID = ?', (productId ))
            conn.commit()
            msg = "Deleted successsfully"
        except:
            conn.rollback()
            msg = "Error occured"
    conn.close()
    print(msg)
    return redirect(url_for('root'))

#@app.route("/displayCategory")
#def displayCategory():
#        loggedIn, firstName, noOfItems = getLoginDetails()
#        categoryId = request.args.get("categoryId")
#        with sqlite3.connect('database.db') as conn:
#            cur = conn.cursor()
#            cur.execute("SELECT products.productId, products.name, products.price, products.image, categories.name FROM products, categories WHERE products.categoryId = categories.categoryId AND categories.categoryId = ?", (categoryId, ))
#            data = cur.fetchall()
#        conn.close()
#        categoryName = data[0][4]
#        data = parse(data)
#        return render_template('displayCategory.html', data=data, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryName=categoryName)





@app.route("/account/profile")
def profileHome():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template("profileHome.html", loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/edit")
def editProfile():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM users WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM users WHERE email = ?", (session['email'], ))
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE users SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("changePassword.html", msg=msg)
    else:
        return render_template("changePassword.html")

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        
        with sqlite3.connect('database.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE users SET firstName = ?, lastName = ? WHERE email = ?', (firstName, lastName, email))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('editProfile'))

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)

@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = request.args.get('productId')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price FROM products WHERE productId = ?', (productId, ))
        productData = cur.fetchone()
    conn.close()
    return render_template("productDescription.html", data=productData, loggedIn = loggedIn, firstName = firstName, noOfItems = noOfItems)



@app.route("/checkout")
def checkout():
    loggedIn, firstName, noOfItems = getLoginDetails()

    if 'email' in session:
        return render_template('checkout.htm',loggedIn = loggedIn,firstName = firstName,noOfItems = noOfItems)
    else:
        return render_template('checkout.htm', error='')














@app.route("/addToCart")
def addToCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        productId = int(request.args.get('productId'))
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM users WHERE email = ?", (session['email'], ))
            userId = cur.fetchone()[0]
            try:
                cur.execute("INSERT INTO kart (userId, productId) VALUES (?, ?)", (userId, productId))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"
        conn.close()
        return redirect(url_for('root'))


























@app.route("/cart")
def cart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price FROM products, kart WHERE products.productId = kart.productId AND kart.userId = ?", (userId, ))
        products = cur.fetchall()
        listproducts = []
        
        nameproducts = []
        for i in range(len(products)):
            listproducts.append(products[i][0])
            nameproducts.append(products[i][1])
        cart_vector = [0]*1681
        for item in listproducts:
            cart_vector[item-1] = 1
            
        cart_np = array(cart_vector)    
        df = pd.read_csv("d_i.csv")
        df = df.drop(columns = ['dish_id','index'])
        np_matrix = df.as_matrix()
        
        
        normalized_cart = np.multiply(u_i_SVD[userId-1],cart_np)
        
        cart_nptr = normalized_cart.T
        
        result = np_matrix.dot(cart_nptr)
        
        
        dish_no = np.argmax(result)
                
        import json
        with open('train.json', 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        chosenCuisine = ["indian", "italian", "mexican","chinese","korean","spanish","greek","british","jamaican"]
        data = df.loc[df["cuisine"].isin(chosenCuisine)]        
        data = data.head(1000)
        data.reset_index()
        
        row =data.iloc[dish_no]
        ing_list = list(row['ingredients'])
        recipe_name = row['id']
        cuisine = row['cuisine']
        
        for items in nameproducts:
           if(items in ing_list):
              ing_list.remove(items)
        ing_list
        with sqlite3.connect('database.db') as conn1:
                cur = conn1.cursor()
                cur.execute("DELETE FROM recommend")
                
        conn1.close()        
        with sqlite3.connect('database.db') as conn2:
            cur2 = conn2.cursor()
            for items in ing_list:
                try:
                    string1 = "INSERT INTO recommend (nitem) VALUES ('" + str(items) + "');"
                    conn2.execute(string1)
                    conn2.commit()
                    msg = "Added successfully"
                except:
                    conn.rollback()
                    msg = "Error occured"
        conn2.close()
            
    with sqlite3.connect('database.db') as conn3:
        cur = conn.cursor()
        cur.execute('SELECT * FROM recommend')
        recommend = cur.fetchall()
        
        
    conn3.close()  
    
    
        
    totalPrice = 0 
    for row in products:
        totalPrice += row[2]
        
    if(totalPrice == 0):
        return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

    return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, recommend=recommend,recipe_name = recipe_name,cuisine = cuisine)


@app.route("/add_recomm")
def add_recomm():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']
    
    
    with sqlite3.connect('database.db') as conn3:
        cur = conn3.cursor()
        cur.execute('SELECT nitem FROM recommend')
        recommend = cur.fetchall()
        
        
    conn3.close()     
    
    
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (session['email'], ))
        userId = cur.fetchone()[0]
        
    conn.close()    
    
    
    for itemname in recommend:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            string1 = "SELECT productId FROM products WHERE name = '" + str(itemname[0]) +"'"
            cur.execute(string1)
            productId = cur.fetchone()[0]
            try:
                cur.execute("INSERT INTO kart (userId, productId) VALUES (?, ?)", (userId, productId))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"
        conn.close()
    with sqlite3.connect('database.db') as conn1:
        cur = conn1.cursor()
        cur.execute("DELETE FROM recommend")
        
    conn1.close()   
    return redirect(url_for('root'))








@app.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']
    productId = int(request.args.get('productId'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        try:
            cur.execute("DELETE FROM kart WHERE userId = ? AND productId = ?", (userId, productId))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('root'))

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))

def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Parse form data    
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        

        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName) VALUES (?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName))

                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("login.html", error=msg)
    
    
    
    
    
@app.route("/add_users", methods=["GET", "POST"])
def add_users():
  
  import pandas as pd
  u_i = pd.read_csv("u_i.csv")
    
  for i,row in u_i.iterrows():
        
    password = 'abcd'
    email = row['dish_id'] + "@sams.com"
    firstName = row['dish_id']
    lastName = "Walmart"
        

    with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName) VALUES (?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName))

                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
    con.close()
  return render_template("login.html", error=msg)
    

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

if __name__ == '__main__':
    app.run(debug=True)
