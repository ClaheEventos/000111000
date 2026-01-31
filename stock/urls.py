from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    # ==================================
    # HOME Y DASHBOARDS
    # ==================================
    path('', views.home, name='home'),
    path('panel-alertas/', views.panel_alertas, name='panel_alertas'),
    
    # ==================================
    # PRODUCTOS
    # ==================================
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('productos/actualizar-stock/<int:producto_id>/', views.actualizar_stock, name='actualizar_stock'),
    
    # ==================================
    # TIPOS DE PRODUCTO
    # ==================================
    path('tipos/crear/', views.crear_tipo, name='crear_tipo'),
    
    # ==================================
    # CLIENTES
    # ==================================
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    
    # ==================================
    # CHOFERES
    # ==================================
    path('choferes/', views.lista_choferes, name='lista_choferes'),
    path('choferes/crear/', views.crear_chofer, name='crear_chofer'),
    path('choferes/editar/<int:chofer_id>/', views.editar_chofer, name='editar_chofer'),
    
    # ==================================
    # 🆕 VENTAS (GESTIÓN COMPLETA)
    # ==================================
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/crear/', views.crear_venta, name='crear_venta'),
    path('ventas/detalle/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('ventas/actualizar-estado/<int:venta_id>/', views.actualizar_estado_venta, name='actualizar_estado_venta'),
    
    # ==================================
    # REPORTES (SOLO VENTAS CONFIRMADAS)
    # ==================================
    path('ventas/consultar/', views.consultar_ventas, name='consultar_ventas'),
    
    # ==================================
    # ENVÍOS (TRACKING OPCIONAL)
    # ==================================
    path('envios/', views.lista_envios, name='lista_envios'),
    path('envios/crear/<int:venta_id>/', views.crear_envio, name='crear_envio'),
    path('envios/detalle/<int:envio_id>/', views.detalle_envio, name='detalle_envio'),
    path('envios/actualizar-estado/<int:envio_id>/', views.actualizar_estado_envio, name='actualizar_estado_envio'),
    path('envios/programa-dia/', views.programa_dia, name='programa_dia'),
    path('envios/asignar-pendientes/', views.asignar_envios_pendientes, name='asignar_envios_pendientes'),

        path('ventas/<int:venta_id>/asignar-chofer/', views.asignar_chofer_venta, name='asignar_chofer_venta'),
    # ==================================
    # IMÁGENES
    # ==================================
    path('imagenes/subir/', views.subir_imagen, name='subir_imagen'),
    path('api/productos/', views.api_productos, name='api_productos'),

       # 🚚 PANEL DE CHOFERES
# 🚚 PANEL DE CHOFERES
    path('chofer/acceso/', views.acceso_chofer, name='acceso_chofer'),

    path('chofer/', views.panel_chofer, name='panel_chofer'),
    path('chofer/venta/<int:venta_id>/', views.chofer_detalle_venta_confirmada, name='chofer_detalle_venta_confirmada'),  # 👈 ESTA LÍNEA
    path('chofer/envio/<int:envio_id>/', views.chofer_detalle_envio, name='chofer_detalle_envio'),
    path('chofer/envio/<int:envio_id>/cambiar-estado/', views.chofer_cambiar_estado_envio, name='chofer_cambiar_estado_envio'),
    path('chofer/historial/', views.chofer_historial, name='chofer_historial'),
    path('chofer/cerrar-sesion/', views.chofer_cerrar_sesion, name='chofer_cerrar_sesion'),
]

