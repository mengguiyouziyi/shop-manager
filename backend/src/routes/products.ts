import { Router } from 'express';
import { authenticateToken, requireRole } from '../middleware/auth';
import { 
  getProducts, 
  getProductById, 
  createProduct, 
  updateProduct, 
  deleteProduct 
} from '../controllers/productController';

const router = Router();

router.get('/', authenticateToken, getProducts);
router.get('/:id', authenticateToken, getProductById);
router.post('/', authenticateToken, requireRole(['admin', 'staff']), createProduct);
router.put('/:id', authenticateToken, requireRole(['admin', 'staff']), updateProduct);
router.delete('/:id', authenticateToken, requireRole(['admin']), deleteProduct);

export { router as productRouter };