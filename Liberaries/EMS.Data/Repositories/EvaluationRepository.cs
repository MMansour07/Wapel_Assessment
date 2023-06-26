using EMS.Core.Interfaces;
using EMS.Core.Model;
using EMS.Data.Identity;

namespace EMS.Data.Repositories
{
    public class EvaluationRepository : Repository<Evaluation>, IEvaluationRepository
    {
        public EvaluationRepository(DataContext dbContext) : base(dbContext)
        {
        }
    }
}
