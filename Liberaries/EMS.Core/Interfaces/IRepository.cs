using EMS.Core.Model;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Threading.Tasks;

namespace EMS.Core.Interfaces
{
    public interface IRepository<T> where T : BaseEntity
    {
        /// <summary>
        /// Get all queries
        /// </summary>
        /// <returns>IQueryable queries</returns>
        Task<List<T>> GetAll();
        Task<T> Add(T entity);

        Task<T> FindByIdAsync(int id);
        IEnumerable<T> AddRange(IEnumerable<T> entities);

        /// <summary>
        /// Find queries by predicate
        /// </summary>
        /// <param name="predicate">search predicate (LINQ)</param>
        /// <returns>IQueryable queries</returns>
        IQueryable<T> FindBy(Expression<Func<T, bool>> predicate);

        /// <summary>
        /// Find entity by keys
        /// </summary>
        /// <param name="keys">search key</param>
        /// <returns>T entity</returns>

        /// <summary>
        /// Add new entity
        /// </summary>
        /// <param name="entity"></param>
        /// <returns></returns>
        //Task AddAsync(T entity);

        /// <summary>
        /// Remove entity from database
        /// </summary>
        /// <param name="entity"></param>

        /// <summary>
        /// Edit entity
        /// </summary>
        /// <param name="entity"></param>
        void UpdateAsync(T entity);

        IQueryable<T> Filter(Expression<Func<T, bool>> filter = null, Sort srt = null, Query qry = null,
            Expression<Func<T, bool>> searchfilter = null, bool anotherLevel = false, string includeProperties = "");

        Task<int> Delete(Expression<Func<T, bool>> predicate = null);

        /// <summary>
        /// Persists all updates to the data source.
        /// </summary>
    }
}
