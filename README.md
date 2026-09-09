# FashionConnect - Hyperlocal Fashion Marketplace for Patna, Bihar

A production-ready location-based multi-vendor marketplace that connects customers with nearby clothing shops in Patna, Bihar. The platform allows local shopkeepers to register their shops, manage products and inventory, and receive customer orders based on GPS location.

## 🌟 Core Features

### For Customers
- **GPS-Based Discovery**: Find fashion products available at nearby local shops based on GPS location
- **Nearby Shops**: Browse shops within 1km, 3km, 5km, 10km radius
- **Smart Search**: Search products, shops, and categories with distance-based results
- **Real-time Inventory**: See available sizes, colors, and stock levels
- **Wishlist & Cart**: Save favorites and manage shopping cart
- **Store Pickup**: Order online and pick up from local shops

### For Sellers (Shopkeepers)
- **Easy Registration**: Simple shop registration with admin approval
- **Product Management**: Add products with images, sizes, colors, and stock
- **Inventory Control**: Real-time stock management with size/color tracking
- **Order Management**: Accept/reject orders and update status
- **Shop Dashboard**: Complete analytics and order tracking
- **GPS Integration**: Set exact shop location for customer discovery

### For Admin
- **Dashboard Analytics**: Complete marketplace statistics
- **Seller Management**: Approve/reject seller registrations
- **Shop Management**: Verify and manage shop listings
- **Product Moderation**: Remove inappropriate products
- **Order Oversight**: View all marketplace orders

## 🏗️ Architecture

### Backend (FastAPI + MongoDB)
- **RESTful APIs**: Clean, modular API structure
- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access**: Admin, Seller, Customer roles with strict permissions
- **Geospatial Queries**: MongoDB 2dsphere index for location-based searches
- **File Upload**: Object storage integration for images
- **Async Operations**: Motor for async MongoDB operations

### Frontend (React + Modern UI)
- **Mobile-First Design**: Responsive across all devices
- **Location Context**: GPS integration with permission handling
- **Real-time Updates**: Live inventory and status updates
- **Modern Components**: Shadcn/ui with Framer Motion animations
- **Context Management**: Auth, Cart, Location contexts

## 📁 Project Structure

```
fashion_connector/
├── backend/
│   ├── config/
│   │   └── database.py          # Database configuration and indexes
│   ├── models/
│   │   └── schemas.py           # Pydantic models for API validation
│   ├── routes/
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── shops.py             # Shop management with geospatial queries
│   │   ├── products.py          # Product management
│   │   ├── admin.py             # Admin endpoints
│   │   ├── wishlist.py          # Wishlist functionality
│   │   ├── cart.py              # Shopping cart
│   │   ├── orders.py            # Order management
│   │   └── categories.py        # Category management
│   ├── middleware/
│   │   └── auth.py              # Authentication middleware
│   ├── utils/
│   │   ├── security.py          # Password hashing and JWT
│   │   └── geo.py               # Geospatial utilities
│   ├── server.py                # Main FastAPI application
│   ├── seed_data.py             # Database seeding script
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ui/              # UI components
    │   │   └── common/          # Shared components
    │   ├── context/
    │   │   ├── AuthContext.jsx  # Authentication state
    │   │   ├── CartContext.jsx   # Shopping cart state
    │   │   └── LocationContext.jsx # GPS location state
    │   ├── pages/
    │   │   ├── customer/        # Customer-facing pages
    │   │   ├── seller/          # Seller dashboard pages
    │   │   └── admin/           # Admin dashboard pages
    │   ├── utils/
    │   │   ├── location.js      # Location utilities
    │   │   └── api.js           # API client
    │   └── App.js               # Main React app
    └── package.json
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- MongoDB 4.4+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
# Edit .env file with your configuration
MONGO_URL=mongodb://localhost:27017
DB_NAME=fashionconnect_db
JWT_SECRET=your-secret-key
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your-password
FRONTEND_URL=http://localhost:3000
```

4. **Initialize database**
```bash
python seed_data.py
```

5. **Start the server**
```bash
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
```bash
# Create .env file
REACT_APP_BACKEND_URL=http://localhost:8000
```

4. **Start the development server**
```bash
npm start
```

## 🗄️ Database Schema

### Users Collection
```javascript
{
  id: string,
  name: string,
  email: string,
  password_hash: string,
  phone: string,
  role: "admin" | "seller" | "customer",
  status: "ACTIVE" | "PENDING" | "SUSPENDED",
  shop_id: string,
  created_at: datetime,
  updated_at: datetime
}
```

### Shops Collection
```javascript
{
  id: string,
  seller_id: string,
  name: string,
  category: string,
  description: string,
  address: string,
  short_address: string,
  plus_code: string,
  phone: string,
  logo_url: string,
  banner_url: string,
  latitude: number,
  longitude: number,
  location: { type: "Point", coordinates: [longitude, latitude] },
  timings: { Monday: "11:00 AM - 10:00 PM", ... },
  services: [string],
  status: "ACTIVE" | "PENDING" | "SUSPENDED",
  rating: number,
  review_count: number,
  created_at: datetime,
  updated_at: datetime
}
```

### Products Collection
```javascript
{
  id: string,
  shop_id: string,
  shop_name: string,
  name: string,
  description: string,
  category: string,
  subcategory: string,
  price: number,
  discount_price: number,
  images: [string],
  sizes: ["S", "M", "L", "XL", "XXL"],
  colors: [string],
  stock: number,
  availability: boolean,
  brand: string,
  size_stock: [{ size: string, stock: number }],
  created_at: datetime,
  updated_at: datetime
}
```

## 🔐 Authentication & Authorization

### JWT-Based Authentication
- Access tokens with 7-day expiration
- Secure HTTP-only cookies
- Role-based middleware protection
- Backend validation on every protected route

### User Roles
- **Admin**: Full marketplace access
- **Seller**: Access to own shop, products, and orders only
- **Customer**: Shopping and order management

## 📍 Geospatial Features

### Location-Based Discovery
- MongoDB 2dsphere index for efficient geospatial queries
- Haversine distance calculation
- Nearby shops within radius (1km, 3km, 5km, 10km)
- Distance-based sorting and filtering

### GPS Integration
- Browser Geolocation API
- Permission handling
- Manual location fallback
- Real-time distance updates

## 📱 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

### Shops
- `GET /api/shops` - List shops with filters
- `GET /api/shops/nearby` - Get nearby shops (GPS)
- `GET /api/shops/featured` - Get featured shops
- `GET /api/shops/:id` - Get shop details
- `POST /api/shops` - Create shop (seller)
- `PUT /api/shops/:id` - Update shop

### Products
- `GET /api/products` - List products with filters
- `GET /api/products/nearby` - Get nearby products (GPS)
- `GET /api/products/:id` - Get product details
- `POST /api/products` - Create product (seller)
- `PUT /api/products/:id` - Update product
- `DELETE /api/products/:id` - Delete product

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders` - List orders
- `GET /api/orders/:id` - Get order details
- `PUT /api/orders/:id/status` - Update order status

### Admin
- `GET /api/admin/dashboard` - Dashboard statistics
- `GET /api/admin/sellers` - List all sellers
- `PUT /api/admin/sellers/:id/approve` - Approve seller
- `PUT /api/admin/shops/:id/approve` - Approve shop

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📦 Deployment

### Backend Deployment
1. Set environment variables in production
2. Build Docker image: `docker build -t fashionconnect-backend .`
3. Deploy to your cloud provider
4. Run database migrations: `python seed_data.py`

### Frontend Deployment
1. Build production bundle: `npm run build`
2. Deploy to Vercel, Netlify, or your hosting provider
3. Set `REACT_APP_BACKEND_URL` to production API URL

## 🔧 Environment Variables

### Backend (.env)
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=fashionconnect_db
JWT_SECRET=your-secret-key
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your-password
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)
```
REACT_APP_BACKEND_URL=http://localhost:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Team

- **Developed for**: Patna, Bihar local fashion marketplace
- **Core Focus**: Hyperlocal commerce with GPS-based discovery

## 🙏 Acknowledgments

- Seed data includes the real "Fashion Hub" shop from Patna
- Additional shops are fictional for demonstration purposes
- Built with modern web technologies and best practices

## 📞 Support

For support and queries:
- Email: support@fashionconnect.com
- Location: Patna, Bihar, India

---

**Note**: This is a production-ready application designed specifically for the Patna, Bihar market. The geospatial features and location-based discovery are optimized for local commerce.