using EMS.Core.Helper;
using EMS.Core.Interfaces;
using EMS.Core.Model;
using EMS.Data.Identity;
using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Linq.Expressions;
using System.Threading.Tasks;

namespace EMS.Data.Repositories
{
    public class Repository<T> : IRepository<T>, IDisposable where T : BaseEntity
    {
        private readonly DataContext _context;
        private readonly DbSet<T> _dbSet;

        public Repository(DataContext context)
        {
            _context = context;
            _dbSet = context.Set<T>();
        }


        public async Task<T> FindByIdAsync(int id)
        {
            return await _dbSet.FirstOrDefaultAsync(x => x.Id == id);
        }

        public virtual IQueryable<T> FindBy(Expression<Func<T, bool>> predicate)
        {
            return _dbSet.Where(predicate);
        }

        public async Task<T> Add(T entity)
        {
            T res = _dbSet.Add(entity);
            await _context.SaveChangesAsync();
            return res;
        }
        public IEnumerable<T> AddRange(IEnumerable<T> entities)
        {
            return _dbSet.AddRange(entities);
        }

        public void UpdateAsync(T entity)
        {
            _dbSet.Attach(entity);

            _context.Entry(entity).State = EntityState.Modified;
        }
        public async Task<int> Delete(Expression<Func<T, bool>> predicate = null)
        {
            return await _dbSet.Where(predicate).DeleteFromQueryAsync();
        }

        public async Task<List<T>> GetAll()
        {
            return await _dbSet.AsNoTracking().ToListAsync();
        }

        public IQueryable<T> Filter(Expression<Func<T, bool>> filter = null, Sort srt = null, Query qry = null,
            Expression<Func<T, bool>> searchfilter = null, bool anotherLevel = false, string includeProperties = "")
        {
            IQueryable<T> query = _dbSet;

            if (filter != null)
            {
                if (!string.IsNullOrEmpty(qry?.generalSearch))
                {
                    var parameter = Expression.Parameter(typeof(T));

                    var leftVisitor = new ReplaceExpressionVisitor(filter.Parameters[0], parameter);
                    var left = leftVisitor.Visit(filter.Body);

                    var rightVisitor = new ReplaceExpressionVisitor(searchfilter.Parameters[0], parameter);
                    var right = rightVisitor.Visit(searchfilter.Body);

                    query = query.Where(Expression.Lambda<Func<T, bool>>(Expression.AndAlso(left, right), parameter));
                }
                else
                    query = query.Where(filter);
            }

            if (!string.IsNullOrEmpty(includeProperties))
            {
                foreach (var includeProperty in includeProperties.Split(new char[] { ',' }, StringSplitOptions.RemoveEmptyEntries))
                {
                    query = query.Include(includeProperty);
                }
            }
            if (!string.IsNullOrEmpty(srt?.field))
            {
                var param = Expression.Parameter(typeof(T), string.Empty);
                var property = Expression.PropertyOrField(param, srt.field);
                var sort = Expression.Lambda(property, param);

                var call = Expression.Call(
                    typeof(Queryable),
                    (!anotherLevel ? "OrderBy" : "ThenBy") + ("desc" == srt.sort ? "Descending" : string.Empty),
                    new[] { typeof(T), property.Type },
                    query.Expression,
                    Expression.Quote(sort));

                return query.Provider.CreateQuery<T>(call);
            }
            
            return query.AsNoTracking();
        }

        private bool disposed = false;

        protected virtual void Dispose(bool disposing)
        {
            if (!this.disposed)
            {
                if (disposing)
                {
                    _context.Dispose();
                }
            }
            this.disposed = true;
        }

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }
    }
}
