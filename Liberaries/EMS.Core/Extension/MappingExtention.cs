using EMS.Core.Interfaces;
using System;
using System.Linq;
using System.Linq.Expressions;

namespace EMS.Core.Extension
{
    internal static class MappingExtention
    {
        internal static IOrderedQueryable<T> Order<T>(this IQueryable<T> source, Sort srt, bool anotherLevel = false)
        {
            if (string.IsNullOrEmpty(srt.field))
                return (IOrderedQueryable<T>)source;

            var param = Expression.Parameter(typeof(T), string.Empty);
            var property = Expression.PropertyOrField(param, srt.field);
            var sort = Expression.Lambda(property, param);

            var call = Expression.Call(
                typeof(Queryable),
                (!anotherLevel ? "OrderBy" : "ThenBy") + ("desc" == srt.sort ? "Descending" : string.Empty),
                new[] { typeof(T), property.Type },
                source.Expression,
                Expression.Quote(sort));

            return (IOrderedQueryable<T>)source.Provider.CreateQuery<T>(call);
        }

        internal static Expression<Func<T, bool>> AndAlso<T>(this Expression<Func<T, bool>> left, Expression<Func<T, bool>> right)
        {
            var param = Expression.Parameter(typeof(T), "x");
            var body = Expression.AndAlso(
                    Expression.Invoke(left, param),
                    Expression.Invoke(right, param)
                );
            var lambda = Expression.Lambda<Func<T, bool>>(body, param);
            return lambda;
        }


    }
}