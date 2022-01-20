from flask import *
import mlab
from mongoengine import *
from models.user import User
from models.shipper import Shipper
from models.product import Product
from models.order import Order
from datetime import datetime
from gmail import *

app = Flask(__name__)
app.secret_key = "techmarket"

mlab.connect1()

# Trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# Đăng nhập/Đăng ký/Đăng xuất USER
@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'GET':    
        return render_template('login/login-user.html')
    elif request.method == 'POST':
        form = request.form 
        username = form['username']
        password = form['password']
        
        found_user = User.objects(username=username,password=password)

        all_users = User.objects()
        if found_user:
            session['user-loggedin'] = True
            user = User.objects.get(username=username)
            session["user_id"] = str(user.id)
            return redirect(url_for('user'))
        else:
            return render_template('login/login-fail.html', template=1)

@app.route('/signup_user', methods=['GET', 'POST'])
def signup_user():
    if request.method == 'GET':
        return render_template('signup/signup-user.html')
    elif request.method == 'POST':
        form = request.form 

        fullname = form['fullname']
        phone = form['phone']
        email = form['email']
        address = form['address']
        username = form['username']
        password = form['password']
        balance = form['balance']

        all_user = User.objects(username=username)

        if len(all_user) > 0:
            return render_template('signup/signup-fail.html', template=1)
        else:
            new_user = User(
                fullname = fullname,
                phone=phone,
                email = email,
                address=address,
                username = username,
                password = password,
                balance=balance
            ) 
            new_user.save()
            
            found_user = User.objects.get(username=username)
            
            html_content = '''
            Chúc mừng bạn đã tạo tài khoản thành công trên hệ thống Tech Fashion.
            Cảm ơn quý khách đã sử dụng dịch vụ của chúng tôi!
            '''
            msg = Message('Tạo tài khoản thành công',to=found_user.email,html=html_content)
            # gmail.send(msg)
            return redirect(url_for('login_user'))

@app.route('/logout_user')
def logout_user():
    if session['user-loggedin'] == False:
        return redirect(url_for('index'))
    else:
        session['user-loggedin'] = False
        del session["user_id"]
        return redirect(url_for('index'))

# Đăng nhập/Đăng ký/Đăng xuất SHIPPER
@app.route('/login_shipper', methods=['GET','POST'])
def login_shipper():
    if request.method == 'GET':
        return render_template('login/login-shipper.html')
    elif request.method == 'POST':
        form = request.form 
        username = form['username']
        password = form['password']

        found_shipper = Shipper.objects(username=username,password=password)

        all_shipper = Shipper.objects()
        if found_shipper:
            session['shipper-loggedin'] = True
            shipper = Shipper.objects.get(username=username)
            session["shipper_id"] = str(shipper.id)
            return redirect(url_for('shipper'))
        else:
            return render_template('login/login-fail.html', template=0)

@app.route('/signup_shipper', methods=['GET','POST'])
def signup_shipper():
    if request.method == 'GET':
        return render_template('signup/signup-shipper.html')
    elif request.method == 'POST':
        form = request.form 

        fullname = form['fullname']
        phone = form['phone']
        email = form['email']
        id_person = form['id_person']
        birthday = form['birthday']
        username = form['username']
        password = form['password']

        all_shipper = Shipper.objects(username=username)
        if len(all_shipper) > 0:
            return render_template('signup/signup-fail.html', template=0)
        else:
            new_shipper = Shipper(
                fullname = fullname,
                phone = phone,
                email = email,
                id_person = id_person,
                birthday = birthday,
                balance = 0,
                username = username,
                password = password
            )
            new_shipper.save()

            found_shipper = Shipper.objects.get(username=username)
            
            html_content = '''
            Tạo tài khoản thành công
            '''
            msg = Message('TECH FASHION',to=found_shipper.email,html=html_content)
            # gmail.send(msg)
            return redirect(url_for('login_shipper'))

@app.route('/logout_shipper')
def logout_shipper():
    if session['shipper-loggedin'] == False:
        return redirect(url_for('index'))
    else:
        session['shipper-loggedin'] = False
        del session["shipper_id"]
        return redirect(url_for('index'))

# Search
# Hiển thị danh sách sản phẩm
@app.route('/search/<search>')
def search(search):
    session['search'] = search
    all_product_type = Product.objects(product_type=search)
    if len(all_product_type) > 0:
        return render_template('search/search.html', all_product=all_product_type)
    else:
        all_product_place = Product.objects(place=search)
        return render_template('search/search.html', all_product=all_product_place)

# Hiển thị chi tiết sản phẩm
@app.route('/detail/<product_id>')
def detail(product_id):
    detail_product = Product.objects.with_id(product_id)
    return render_template('search/detail.html', detail_product=detail_product)

# User
# Giao diện chính cho User
@app.route('/user')
def user():
    if "user-loggedin" in session:
        if session['user-loggedin'] == True:
            return render_template('user.html')
        else:
            return redirect(url_for('login_user'))
    else:
        return redirect(url_for('login_user'))

# Thông tin cá nhân User
@app.route('/user_information')
def user_information():
    found_user = User.objects.with_id(session["user_id"])
    if found_user is not None:
        return render_template('user/information.html', found_user=found_user)
    else:
        return 'User is not found'

# Cập nhật thông tin User
@app.route('/user_update', methods=['GET','POST'])
def user_update():
    update_user = User.objects.with_id(session['user_id'])
    if update_user is not None:
        if request.method == 'GET':
            return render_template('user/user-update.html',update_user=update_user)
        elif request.method == 'POST':
            form = request.form

            phone = form['phone']
            email = form['email']
            address = form['address']
            password = form['password']

            update_user.update(set__phone=phone)
            update_user.update(set__email=email)
            update_user.update(set__address=address)
            update_user.update(set__password=password)
    else:
        return 'User is not found'
    return redirect(url_for('user_information'))

# Nạp tiền cho tài khoản
@app.route('/add_money', methods = ['GET','POST'])
def add_money():
    if request.method == 'GET':
        found_user = User.objects.with_id(session["user_id"])
        return render_template('user/add-money.html', found_user=found_user)
    elif request.method == 'POST':
        found_user = User.objects.with_id(session["user_id"])
        ex_money = int(found_user.balance)

        form = request.form
        money = int(form['money'])
        found_user.update(set__balance = money + ex_money)
        return redirect(url_for('add_money'))

# Thêm một sản phẩm vào giỏ hàng
@app.route('/add_order/<product_id>', methods=['GET','POST'])
def add_order(product_id):
    if "shipper-loggedin" in session and session['shipper-loggedin'] == True:
        return render_template('shipper/cart-fail.html')
    if "user-loggedin" in session:
        if session['user-loggedin'] == True:
            found_user = User.objects.get(id = session['user_id'])
            found_product = Product.objects.with_id(product_id)
            found_order = Order.objects(user_id=session['user_id'], is_ordered=False, status="Shipper chưa nhận đơn")

            if found_product is not None:
                if len(found_order) > 0:
                    ex_fee = found_order[0].order_fee
                    
                    found_order.update(
                        add_to_set__product_id=product_id,
                        set__order_time=datetime.now(),
                        set__order_fee=int(found_product.price)+int(ex_fee),
                        set__ship_fee=0.1*int(int(found_product.price)+int(ex_fee))
                    )
                    return redirect(url_for('search', search=session['search']))
                else:
                    add_order = Order(
                        user_id=[session['user_id']],
                        product_id=[product_id],
                        address=found_user.address,
                        order_time=datetime.now(),
                        order_fee=int(found_product.price),
                        ship_fee=0.1*int(found_product.price),
                        is_ordered=False,
                        status="Shipper chưa nhận đơn"
                    )
                    add_order.save()
                    return redirect(url_for('search', search=session['search']))
            else: 
                return 'Product is not found'
        else:
            return redirect(url_for('login_user'))
    else:
        return redirect(url_for('login_user'))

# Hiển thị giỏ hàng
@app.route('/cart', methods=['GET','POST'])
def cart():
    found_order = Order.objects(user_id=session['user_id'], is_ordered=False, status="Shipper chưa nhận đơn")
    if request.method == 'GET':
        if len(found_order) > 0:
            cart = found_order[0]
            order_product = cart.product_id
            return render_template('user/cart.html', cart=cart, order_product=order_product, template=1)
        else:
            return render_template('user/cart.html', template=0)
    elif request.method == 'POST':
        form = request.form
        request_time = form['request_time']
        found_order.update(set__request_time=request_time)
    return redirect(url_for('cart'))

# Gửi yêu cầu mua đơn hàng
@app.route('/ordered/<order_id>')
def ordered(order_id):
    found_order = Order.objects.with_id(order_id)
    if found_order is not None:
        found_user = found_order.user_id
        total = int(found_order.order_fee) + int(found_order.ship_fee)
        ex_balance = found_user[0].balance
        if ex_balance >= total:
            # Trừ tiền
            found_user[0].update(set__balance = ex_balance - total)
            found_order.update(set__is_ordered=True)
            # Gửi Mail
            
            html_content='''Đơn hàng của bạn đã được gửi đi,
                        Tài khoản của bạn sẽ bị trừ đi {{total}}$ tổng chi phí sản phẩm và vận chuyển của đơn hàng này.
                        Cảm ơn bạn đã sử dụng dịch vụ của TechFashion'''
            html_content1 = html_content.replace("{{total}}", str(total))
            msg = Message(
                'GỬI YÊU CẦU',
                to=found_user[0].email,
                html=html_content1
            )
            # gmail.send(msg)
            return render_template('user/accepted.html', template=1)
        else:
            return render_template('user/accepted.html', template=0)
    else:
        'Order is not found'

# Hiển thị trạng thái đơn hàng đã yêu cầu
@app.route('/order_status')
def order_status():
    all_order = Order.objects(user_id=session['user_id'], is_ordered=True)
    if len(all_order) > 0:
        return render_template('user/order-status.html', all_order=all_order, template=1)
    else:
        return render_template('user/order-status.html', template=0)

# Cập nhật địa chỉ ship đơn hàng
@app.route('/update_address', methods = ['GET','POST'])
def update_address():
    found_order = Order.objects(user_id=session['user_id'], is_ordered=False, status="Shipper chưa nhận đơn")
    if request.method == 'GET':
        return render_template('user/update-address.html',found_order=found_order[0])
    elif request.method == 'POST':
        form = request.form

        address = form['address']

        found_order.update(set__address=address)
    return redirect(url_for('cart'))

# Xóa một sản phẩm khỏi giỏ hàng
@app.route('/delete_product/<product_id>')
def delete_product(product_id):
    found_order_list = Order.objects(user_id=session['user_id'], is_ordered=False, status="Shipper chưa nhận đơn")
    found_order = found_order_list[0]
    found_product_list = Product.objects(id=product_id)
    found_product = found_product_list[0]

    ex_order_fee = found_order.order_fee
    new_order_fee = found_order.order_fee - found_product.price
    new_ship_fee = 0.1 * new_order_fee
    order_product = found_order.product_id

    for index, product in enumerate(order_product):
        ID = str(product.id)
        if ID == product_id:
            a = list(order_product)
            a.pop(index)
            found_order.update(set__product_id = a, set__order_fee=new_order_fee, set__ship_fee=new_ship_fee)

    found_order_list1 = Order.objects(user_id=session['user_id'], is_ordered=False, status="Shipper chưa nhận đơn")
    found_order1 = found_order_list1[0]

    if len(found_order1.product_id) == 0:
        found_order1.delete()
    return redirect(url_for('cart'))

# User xác nhận đã nhận được hàng
@app.route('/receive_order/<order_id>')
def receive_order(order_id):
    found_order = Order.objects.with_id(order_id)
    if found_order is not None:
        # Chuyển trạng thái đơn
        found_order.update(set__status = "User đã nhận hàng", set__is_ordered=False)
        # Add phí vận chuyển cho Shipper
        found_shipper = found_order.shipper_id
        ship_fee = found_order.ship_fee
        if found_shipper[0].balance == 0:
            found_shipper[0].update(set__balance = ship_fee)
        else: 
            found_shipper[0].update(set__balance = found_shipper[0].balance + ship_fee)
        # Gửi mail cho Shipper
        
        html_content='''Bạn đã vận chuyển thành công đơn hàng đến tay người dùng
                    Bạn sẽ nhận được {{ship_fee}}$ phí ship cho đơn hàng này.
                    Cảm ơn bạn đã tham gia vào hệ thống của TechFashion'''
        html_content1 = html_content.replace("{{ship_fee}}", str(ship_fee))
        msg = Message(
            'NHẬN ĐƠN',
            to=found_shipper[0].email,
            html=html_content1
        )
        # gmail.send(msg)
        return redirect(url_for('order_status'))
    else:
        return 'Order is not found'

# Hiển thị lịch sử mua hàng
@app.route('/order_history')
def order_history():
    all_order = Order.objects(user_id=session['user_id'], is_ordered=False, status="User đã nhận hàng")
    if len(all_order) > 0:
        return render_template('user/order-history.html', all_order=all_order, template=1)
    else:
        return render_template('user/order-history.html', template=0)

# Shipper
# Giao diện chính cho Shipper
@app.route('/shipper')
def shipper():
    if "shipper-loggedin" in session:
        if session['shipper-loggedin'] == True:
            return render_template('shipper.html')
        else:
            return redirect(url_for('login_shipper'))
    else:
        return redirect(url_for('login_shipper'))

# Thông tin cá nhân Shipper
@app.route('/shipper_information')
def shipper_information():
    found_shipper = Shipper.objects.with_id(session["shipper_id"])
    if found_shipper is not None:
        return render_template('shipper/information.html', found_shipper=found_shipper)
    else:
        return 'Shipper is not found'

# Cập nhật thông tin cá nhân cho Shipper
@app.route('/shipper_update', methods=['GET','POST'])
def shipper_update():
    update_shipper = Shipper.objects.with_id(session['shipper_id'])
    if update_shipper is not None:
        if request.method == 'GET':
            return render_template('shipper/shipper-update.html',update_shipper=update_shipper)
        elif request.method == 'POST':
            form = request.form

            phone = form['phone']
            email = form['email']
            password = form['password']

            update_shipper.update(set__phone=phone)
            update_shipper.update(set__email=email)
            update_shipper.update(set__password=password)
    else:
        return 'Shipper is not found'
    return redirect(url_for('shipper_information'))

# Các đơn hàng hiện có cho shipper
@app.route('/ship_request')
def ship_request():
    all_order = Order.objects(is_ordered=True, status="Shipper chưa nhận đơn")
    if len(all_order) > 0:      
        return render_template('shipper/ship-request.html', all_order=all_order,template=1)
    else:
        return render_template('shipper/ship-request.html',template=0)

# Chi tiết đơn hàng
@app.route('/detail_request/<order_id>')
def detail_request(order_id):
    found_order = Order.objects.with_id(order_id)
    if found_order is not None:
        found_user = found_order.user_id  
        order_product = found_order.product_id
        return render_template('shipper/detail-request.html',found_order=found_order,found_user=found_user,order_product=order_product)
    else:
        return 'Order is not found'

# Lịch sử ship đơn hàng
@app.route('/shipped_history')
def shipped_history():
    all_order = Order.objects(shipper_id=session['shipper_id'],status="User đã nhận hàng")
    if len(all_order)>0:
        return render_template('shipper/shipped-history.html',all_order=all_order,template=1)
    else:
        return render_template('shipper/shipped-history.html',template=0)

# Shipper nhận đơn hàng
@app.route('/shipper_accepted_order/<order_id>')
def shipper_accepted_order(order_id):
    found_order = Order.objects.with_id(order_id)
    if found_order is not None:
        found_user = found_order.user_id
        # Thêm ID của Shipper vào đơn
        found_order.update(add_to_set__shipper_id=session['shipper_id'])
        # Đổi trạng thái đơn
        found_order.update(set__status="Shipper đã nhận đơn, đang tiến hành lấy hàng")
        # Gửi Mail cho User
       
        html_content='''Đơn hàng của bạn đã được Shipper chấp nhận giao hàng, vui lòng kiểm tra tình trạng đơn.
                    Cảm ơn bạn đã sử dụng dịch vụ của TechFashion'''
        msg = Message(
            'NHẬN ĐƠN',
            to=found_user[0].email,
            html=html_content
        )
        # gmail.send(msg)
        return redirect(url_for('ship_request'))
    else:
        return 'Order is not found'

# Xem thông tin đơn hiện tại Shipper chấp nhận vận chuyển
@app.route('/ship_status/<status>')
def ship_status(status):
    found_order = Order.objects(shipper_id=session['shipper_id'], status=status)
    if len(found_order) > 0:
        return render_template('shipper/ship-status.html', found_order=found_order, template=1)
    else:
        return render_template('shipper/ship-status.html', template=0)

# Hai nút tìm kiếm tình trạng các đơn Shipper đã nhận
@app.route('/ship_status_select')
def ship_status_select():
    return render_template('shipper/ship-status-select.html')

# Shipper xác nhận đã lấy hàng
@app.route('/product_request/<order_id>')
def product_request(order_id):
    found_order = Order.objects.with_id(order_id)
    if found_order is not None:
        found_user = found_order.user_id
        found_order.update(set__status="Shipper đã nhận hàng, bắt đầu tiến hành vận chuyển")
       
        msg = Message('LẤY HÀNG',to=found_user[0].email,html="Shipper đã lấy được hàng, bắt đầu vận chuyển đến bạn")
        # gmail.send(msg)
        return redirect(url_for('ship_status_select'))
    else:
        return 'Order is not found'

if __name__ == '__main__':
  app.run()