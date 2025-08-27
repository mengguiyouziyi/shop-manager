import { Router } from 'express';
import { authenticateToken } from '../middleware/auth';
import { 
  getMembers, 
  getMemberById, 
  createMember, 
  updateMember, 
  rechargeMember 
} from '../controllers/memberController';

const router = Router();

router.get('/', authenticateToken, getMembers);
router.get('/:id', authenticateToken, getMemberById);
router.post('/', authenticateToken, createMember);
router.put('/:id', authenticateToken, updateMember);
router.post('/:id/recharge', authenticateToken, rechargeMember);

export { router as memberRouter };