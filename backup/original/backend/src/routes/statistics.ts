import { Router } from 'express';
import { authenticateToken } from '../middleware/auth';
import { 
  getSalesStatistics, 
  getProductRanking, 
  getStaffPerformance 
} from '../controllers/statisticsController';

const router = Router();

router.get('/sales', authenticateToken, getSalesStatistics);
router.get('/products/ranking', authenticateToken, getProductRanking);
router.get('/staff/performance', authenticateToken, getStaffPerformance);

export { router as statisticsRouter };