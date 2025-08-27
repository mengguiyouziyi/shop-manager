import { Router } from 'express';
import { authenticateToken } from '../middleware/auth';
import { 
  getOrders, 
  getOrderById, 
  createOrder, 
  updateOrder 
} from '../controllers/orderController';

const router = Router();

router.get('/', authenticateToken, getOrders);
router.get('/:id', authenticateToken, getOrderById);
router.post('/', authenticateToken, createOrder);
router.put('/:id', authenticateToken, updateOrder);

export { router as orderRouter };