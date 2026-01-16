# 🧪 Guía de Testing - Marketplace UCE

## URLs del Sistema
- **Frontend**: http://localhost:5173
- **API Gateway**: http://localhost:8000
- **Grafana**: http://localhost:3000
- **Prometheus**: http://localhost:9090

## Credenciales de Prueba

### Admin
- **Email**: admin@uce.edu.ec
- **Password**: admin123

## Productos de Prueba Disponibles

Los siguientes productos están pre-cargados en la base de datos:

1. **Laptop Gaming** - $1,200.00
   - Descripción: High-performance laptop for gaming and development
   
2. **Wireless Mouse** - $35.99
   - Descripción: Ergonomic wireless mouse with long battery life

3. **USB-C Hub** - $45.00
   - Descripción: 7-in-1 USB-C hub with multiple ports

4. **Mechanical Keyboard** - $150.00
   - Descripción: RGB mechanical keyboard with custom switches

---

## 📋 Checklist de Pruebas

### 1. ✅ Búsqueda de Productos
- [ ] Navegar a `http://localhost:5173/search`
- [ ] Ingresar "Laptop" en el buscador
- [ ] Verificar que aparezca "Laptop Gaming"
- [ ] Probar búsqueda por precio (Min: 40, Max: 200)
- [ ] Probar ordenamiento (Price Low-High, Price High-Low, etc.)

### 2. ✅ Carrito de Compras
- [ ] Ir a Home (http://localhost:5173)
- [ ] Hacer clic en "🛒 Add to Cart" en un producto
- [ ] Verificar que el contador del carrito se actualice
- [ ] Ir al carrito (http://localhost:5173/cart)
- [ ] Aumentar/disminuir cantidad
- [ ] Eliminar producto del carrito

### 3. ✅ Checkout y PayPal
- [ ] En la página del carrito, hacer clic en "💳 Checkout"
- [ ] Llenar el formulario de facturación:
  - First Name: Jorge
  - Last Name: Sanchez
  - Email: jasanchez@gmail.com
  - Phone: 0960249628
  - Address: Cristo Rey
  - City: Quito
  - ZIP Code: 170403
  - Country: Ecuador
- [ ] Verificar que aparezca el botón de PayPal
- [ ] Hacer clic en el botón de PayPal
- [ ] Completar el pago en PayPal (Sandbox)

### 4. ✅ Autenticación y Carrito
- [ ] Agregar productos al carrito
- [ ] Hacer logout (Navbar → Logout)
- [ ] Verificar que el carrito se limpie
- [ ] Hacer login con otra cuenta
- [ ] Verificar que el carrito esté vacío

### 5. ✅ Perfil y Reviews
- [ ] Hacer login
- [ ] Hacer clic en el usuario (Navbar → 👤 buyer ▼)
- [ ] Hacer clic en "Profile" y verificar que se abra la página
- [ ] Hacer clic en "My Reviews" y verificar que se abra la página
- [ ] No debe redirigir a Home

### 6. ✅ Datos Persistentes
- [ ] Agregar producto al carrito
- [ ] Refrescar la página (F5)
- [ ] Verificar que el carrito siga visible (opcional - puede implementarse persistencia)
- [ ] Cambiar de página y volver
- [ ] Verificar que el carrito se mantenga

---

## 🔧 Comandos Útiles

### Ver Logs de Servicios
```bash
# Order Service
docker-compose logs order-service -f

# Payment Service
docker-compose logs payment-service -f

# Product Service
docker-compose logs product-service -f

# Gateway
docker-compose logs gateway -f
```

### Insertar Más Productos
```bash
docker-compose exec mongo mongosh --db marketplace --eval "
db.products.insertOne({
  _id: 'prod-5',
  title: 'Tu Producto',
  description: 'Descripción del producto',
  price: 99.99,
  seller_id: 'seller-1',
  seller_name: 'Mi Tienda',
  status: 'active',
  images: [],
  category: 'Categoría'
});
"
```

### Limpiar Productos
```bash
docker-compose exec mongo mongosh --db marketplace --eval "db.products.deleteMany({});"
```

---

## 📊 Problemas Conocidos y Soluciones

### Problema: "No products found" en Search
**Solución**: 
1. Verificar que hay productos en MongoDB: `docker-compose exec mongo mongosh --db marketplace --eval "db.products.count()"`
2. Reiniciar el frontend: Kill el servidor dev y ejecutar `npm run dev` nuevamente

### Problema: PayPal button no aparece
**Solución**:
1. Llenar COMPLETAMENTE el formulario de checkout
2. Esperar a que aparezca el mensaje "Loading PayPal..."
3. El botón debe aparecer automáticamente

### Problema: Profile/Reviews redirige a Home
**Solución**:
1. Asegurarse de estar logueado
2. El rol debe ser "buyer", "seller" o "admin"
3. Revisar la consola del navegador (F12) para ver errores

### Problema: Carrito se mantiene al cambiar cuenta
**Solución**:
1. Esta es una corrección reciente - el carrito debe limpiarse al logout
2. Si no funciona: Limpiar localStorage (F12 → Storage → Local Storage → Clear)

---

## 🚀 Stack Tecnológico

### Frontend
- React 18 + TypeScript
- Vite (Build tool)
- TailwindCSS (Styling)
- Zustand (State management)
- React Router (Routing)
- Axios (HTTP client)

### Backend
- FastAPI (Python)
- Docker & Docker Compose
- PostgreSQL (Auth/Orders)
- MongoDB (Products)
- Redis (Caching)
- Kafka (Message queue)
- PayPal SDK

---

## 📞 Soporte

Si encuentras problemas:
1. Revisar los logs: `docker-compose logs -f`
2. Verificar que todos los containers estén corriendo: `docker-compose ps`
3. Limpiar caché del navegador: Ctrl+Shift+Del
4. Reiniciar los servicios: `docker-compose restart`
