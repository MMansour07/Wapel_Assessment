using EMS.Core.Interfaces;
using EMS.Core.Model;
using EMS.Data.Identity;
using EMS.Data.Repositories;
using Microsoft.AspNet.Identity.EntityFramework;
using System.Threading.Tasks;

namespace EMS.Data.Unity
{
    public class UnitOfWork : IUnitOfWork
    {
        private readonly DataContext _context;

        private IEvaluationRepository _evaluationRepository;
        private IAuthRepository _authRepository;
        public UnitOfWork(DataContext context)
        {
            _context = context;
        }

        public IEvaluationRepository evaluationRepository
        {
            get
            {
                if (_evaluationRepository == null)
                    _evaluationRepository = new EvaluationRepository(_context);

                return _evaluationRepository;
            }
        }

        public IAuthRepository authRepository
        {
            get
            {
                if (_authRepository == null)
                    _authRepository = new AuthRepository(_context, new ApplicationUserManager(new UserStore<User>(_context)));

                return _authRepository;
            }
        }
        public async Task<int> SaveChanges()
        {
            return await _context.SaveChangesAsync();
        }
    }
}