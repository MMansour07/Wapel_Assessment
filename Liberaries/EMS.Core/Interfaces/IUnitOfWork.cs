
using System.Threading.Tasks;

namespace EMS.Core.Interfaces
{
    public interface IUnitOfWork
    {
        IEvaluationRepository evaluationRepository { get; }
        IAuthRepository authRepository { get; }
        //IMediaRepository mediaRepository { get; }
        Task<int> SaveChanges();
    }
}
