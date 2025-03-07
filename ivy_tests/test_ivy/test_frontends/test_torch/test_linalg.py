# global
import sys
import numpy as np
from hypothesis import strategies as st


# local
import ivy
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import assert_all_close
from ivy_tests.test_ivy.helpers import handle_frontend_test
from ivy_tests.test_ivy.test_frontends.test_torch.test_miscellaneous_ops import (
    dtype_value1_value2_axis,
)


# helpers
@st.composite
def _get_dtype_and_square_matrix(draw):
    dim_size = draw(helpers.ints(min_value=2, max_value=5))
    dtype = draw(helpers.get_dtypes("float", index=1, full=False))
    mat = draw(
        helpers.array_values(
            dtype=dtype[0], shape=(dim_size, dim_size), min_value=0, max_value=10
        )
    )
    return dtype, mat


@st.composite
def _get_dtype_and_matrix(draw):
    arbitrary_dims = draw(helpers.get_shape(max_dim_size=5))
    random_size = draw(st.integers(min_value=1, max_value=4))
    shape = (*arbitrary_dims, random_size, random_size)
    return draw(
        helpers.dtype_and_values(
            available_dtypes=helpers.get_dtypes("float"),
            shape=shape,
            min_value=-10,
            max_value=10,
        )
    )


# vector_norm
@handle_frontend_test(
    fn_tree="torch.linalg.vector_norm",
    dtype_values_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("float"),
        valid_axis=True,
        min_value=-1e04,
        max_value=1e04,
    ),
    kd=st.booleans(),
    ord=helpers.ints(min_value=1, max_value=2),
    dtype=helpers.get_dtypes("valid"),
)
def test_torch_vector_norm(
    *,
    dtype_values_axis,
    kd,
    ord,
    dtype,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    dtype, x, axis = dtype_values_axis
    helpers.test_frontend_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        ord=ord,
        dim=axis,
        keepdim=kd,
        dtype=dtype[0],
    )


# inv
@handle_frontend_test(
    fn_tree="torch.linalg.inv",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=-1e4,
        max_value=1e4,
        small_abs_safety_factor=3,
        shape=helpers.ints(min_value=2, max_value=10).map(lambda x: tuple([x, x])),
    ).filter(lambda x: np.linalg.cond(x[1]) < 1 / sys.float_info.epsilon),
)
def test_torch_inv(
    *,
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        all_aliases=["inverse"],
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        rtol=1e-03,
        atol=1e-02,
        input=x[0],
    )


# inv_ex
@handle_frontend_test(
    fn_tree="torch.linalg.inv_ex",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float", index=1, full=True),
        min_value=0,
        max_value=20,
        shape=helpers.ints(min_value=2, max_value=10).map(lambda x: tuple([x, x])),
    ).filter(lambda x: np.linalg.cond(x[1]) < 1 / sys.float_info.epsilon),
)
def test_torch_inv_ex(
    *,
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        rtol=1e-03,
        atol=1e-02,
        input=x[0],
    )


# pinv
@handle_frontend_test(
    fn_tree="torch.linalg.pinv",
    dtype_and_input=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_num_dims=2,
        min_value=-1e4,
        max_value=1e4,
    ),
)
def test_torch_pinv(
    *,
    dtype_and_input,
    num_positional_args,
    as_variable,
    native_array,
    frontend,
    fn_tree,
    on_device,
):
    input_dtype, x = dtype_and_input
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        native_array_flags=native_array,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        atol=1e-02,
    )


# det
@handle_frontend_test(
    fn_tree="torch.linalg.det",
    dtype_and_x=_get_dtype_and_square_matrix(),
)
def test_torch_det(
    *,
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        all_aliases=["det"],
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x,
    )


# qr
@handle_frontend_test(
    fn_tree="torch.linalg.qr",
    dtype_and_input=_get_dtype_and_matrix(),
)
def test_torch_qr(
    *,
    dtype_and_input,
    num_positional_args,
    as_variable,
    native_array,
    frontend,
    fn_tree,
    on_device,
):
    input_dtype, x = dtype_and_input
    ret, frontend_ret = helpers.test_frontend_function(
        input_dtypes=input_dtype,
        native_array_flags=native_array,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        test_values=False,
    )
    ret = [ivy.to_numpy(x) for x in ret]
    frontend_ret = [np.asarray(x) for x in frontend_ret]

    q, r = ret
    frontend_q, frontend_r = frontend_ret

    assert_all_close(
        ret_np=q @ r,
        ret_from_gt_np=frontend_q @ frontend_r,
        rtol=1e-2,
        atol=1e-2,
        ground_truth_backend=frontend,
    )


# slogdet
@handle_frontend_test(
    fn_tree="torch.linalg.slogdet",
    dtype_and_x=_get_dtype_and_square_matrix(),
)
def test_torch_slogdet(
    *,
    dtype_and_x,
    as_variable,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=False,
        all_aliases=["slogdet"],
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x,
    )


@st.composite
def _get_symmetrix_matrix(draw):
    input_dtype = draw(st.shared(st.sampled_from(draw(helpers.get_dtypes("float")))))
    random_size = draw(helpers.ints(min_value=2, max_value=4))
    batch_shape = draw(helpers.get_shape(min_num_dims=1, max_num_dims=3))
    num_independnt_vals = int((random_size**2) / 2 + random_size / 2)
    array_vals_flat = np.array(
        draw(
            helpers.array_values(
                dtype=input_dtype,
                shape=tuple(list(batch_shape) + [num_independnt_vals]),
                min_value=2,
                max_value=5,
            )
        )
    )
    array_vals = np.zeros(batch_shape + (random_size, random_size))
    c = 0
    for i in range(random_size):
        for j in range(random_size):
            if j < i:
                continue
            array_vals[..., i, j] = array_vals_flat[..., c]
            array_vals[..., j, i] = array_vals_flat[..., c]
            c += 1
    return [input_dtype], array_vals


# eigvalsh
@handle_frontend_test(
    fn_tree="torch.linalg.eigvalsh",
    dtype_x=_get_symmetrix_matrix(),
    UPLO=st.sampled_from(("L", "U")),
)
def test_torch_eigvalsh(
    *,
    dtype_x,
    UPLO,
    num_positional_args,
    as_variable,
    native_array,
    frontend,
    fn_tree,
    on_device,
):
    input_dtype, x = dtype_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        native_array_flags=native_array,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x,
        UPLO=UPLO,
        atol=1e-4,
        rtol=1e-3,
    )


# matrix_power
@handle_frontend_test(
    fn_tree="torch.linalg.matrix_power",
    dtype_and_x=_get_dtype_and_square_matrix(),
    n=helpers.ints(min_value=2, max_value=5),
)
def test_torch_matrix_power(
    *,
    dtype_and_x,
    n,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        all_aliases=["matrix_power"],
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        rtol=1e-01,
        input=x,
        n=n,
    )


# matrix_norm
@handle_frontend_test(
    fn_tree="torch.linalg.matrix_norm",
    dtype_and_x=helpers.dtype_and_values(
        num_arrays=1,
        available_dtypes=helpers.get_dtypes("float"),
        min_num_dims=2,
        max_num_dims=3,
        min_dim_size=1,
        max_dim_size=5,
        min_value=-1e20,
        max_value=1e20,
        large_abs_safety_factor=10,
        small_abs_safety_factor=10,
        safety_factor_scale="log",
    ),
    ord=st.sampled_from(["fro", "nuc", np.inf, -np.inf, 1, -1, 2, -2]),
    keepdim=st.booleans(),
    axis=st.just((-2, -1)),
    dtype=helpers.get_dtypes("float", none=True, full=False),
)
def test_torch_matrix_norm(
    *,
    dtype_and_x,
    ord,
    keepdim,
    axis,
    dtype,
    num_positional_args,
    as_variable,
    with_out,
    native_array,
    frontend,
    fn_tree,
    on_device,
):
    input_dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        native_array_flags=native_array,
        as_variable_flags=as_variable,
        with_out=with_out,
        all_aliases=["matrix_norm"],
        num_positional_args=num_positional_args,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        rtol=1e-04,
        atol=1e-04,
        input=x[0],
        ord=ord,
        dim=axis,
        keepdim=keepdim,
        dtype=dtype[0],
    )


# cross
@handle_frontend_test(
    fn_tree="torch.linalg.cross",
    dtype_input_other_dim=dtype_value1_value2_axis(
        available_dtypes=helpers.get_dtypes("float"),
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=3,
        max_dim_size=3,
        min_value=-1e3,
        max_value=1e3,
        abs_smallest_val=0.01,
        large_abs_safety_factor=2,
        safety_factor_scale="log",
    ),
)
def test_torch_cross(
    dtype_input_other_dim,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    frontend,
    fn_tree,
):
    dtype, input, other, dim = dtype_input_other_dim
    helpers.test_frontend_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        rtol=1e-2,
        atol=1e-3,
        input=input,
        other=other,
        dim=dim,
    )


@st.composite
def _matrix_rank_helper(draw):
    dtype_x = draw(
        helpers.dtype_and_values(
            available_dtypes=helpers.get_dtypes("float"),
            min_num_dims=2,
            min_value=-1e05,
            max_value=1e05,
        )
    )
    return dtype_x


# matrix_rank
@handle_frontend_test(
    fn_tree="torch.linalg.matrix_rank",
    dtype_and_x=_matrix_rank_helper(),
    atol=st.floats(min_value=1e-5, max_value=0.1, exclude_min=True, exclude_max=True),
    rtol=st.floats(min_value=1e-5, max_value=0.1, exclude_min=True, exclude_max=True),
)
def test_matrix_rank(
    dtype_and_x,
    rtol,
    atol,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        all_aliases=["matrix_rank"],
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        rtol=rtol,
        atol=atol,
    )


@handle_frontend_test(
    fn_tree="torch.linalg.cholesky",
    dtype_and_x=_get_dtype_and_square_matrix(),
    upper=st.booleans(),
)
def test_torch_cholesky(
    *,
    dtype_and_x,
    upper,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    dtype, x = dtype_and_x
    x = np.matmul(x.T, x) + np.identity(x.shape[0])  # make symmetric positive-definite

    helpers.test_frontend_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        all_aliases=["cholesky"],
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        rtol=1e-01,
        input=x,
        upper=upper,
    )


# svd
@handle_frontend_test(
    fn_tree="torch.linalg.svd",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=0,
        max_value=10,
        shape=helpers.ints(min_value=2, max_value=5).map(lambda x: tuple([x, x])),
    ),
    full_matrices=st.booleans(),
)
def test_torch_svd(
    *,
    dtype_and_x,
    full_matrices,
    with_out,
    num_positional_args,
    as_variable,
    native_array,
    frontend,
    fn_tree,
    on_device,
):
    dtype, x = dtype_and_x
    x = np.asarray(x[0], dtype=dtype[0])
    # make symmetric positive definite beforehand
    x = np.matmul(x.T, x) + np.identity(x.shape[0]) * 1e-3
    ret, frontend_ret = helpers.test_frontend_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        test_values=False,
        atol=1e-03,
        rtol=1e-05,
        A=x,
        full_matrices=full_matrices,
    )
    ret = [ivy.to_numpy(x) for x in ret]
    frontend_ret = [np.asarray(x) for x in frontend_ret]

    u, s, vh = ret
    frontend_u, frontend_s, frontend_vh = frontend_ret

    assert_all_close(
        ret_np=u @ np.diag(s) @ vh,
        ret_from_gt_np=frontend_u @ np.diag(frontend_s) @ frontend_vh,
        rtol=1e-2,
        atol=1e-2,
        ground_truth_backend=frontend,
    )


# eig
@handle_frontend_test(
    fn_tree="torch.linalg.eig",
    dtype_and_input=_get_dtype_and_square_matrix(),
)
def test_torch_eig(
    *,
    dtype_and_input,
    num_positional_args,
    as_variable,
    native_array,
    frontend,
    fn_tree,
    on_device,
):
    input_dtype, x = dtype_and_input
    x = np.matmul(x.T, x) + np.identity(x.shape[0]) * 1e-3
    if x.dtype == ivy.float32:
        x = x.astype("float64")
        input_dtype = [ivy.float64]
    ret, frontend_ret = helpers.test_frontend_function(
        input_dtypes=input_dtype,
        native_array_flags=native_array,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        test_values=False,
        input=x,
    )
    ret = [ivy.to_numpy(x).astype("float64") for x in ret]
    frontend_ret = [np.asarray(x, dtype=np.float64) for x in frontend_ret]

    l, v = ret
    front_l, front_v = frontend_ret

    assert_all_close(
        ret_np=v @ np.diag(l) @ np.linalg.inv(v),
        ret_from_gt_np=front_v @ np.diag(front_l) @ np.linalg.inv(front_v),
        rtol=1e-2,
        atol=1e-2,
        ground_truth_backend=frontend,
    )


# svdvals
@handle_frontend_test(
    fn_tree="torch.linalg.svdvals",
    dtype_and_x=_get_dtype_and_square_matrix(),
)
def test_torch_svdvals(
    *,
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        A=x,
    )


# solve
@handle_frontend_test(
    fn_tree="torch.linalg.solve",
    dtype_and_data=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=0,
        max_value=10,
        shape=helpers.ints(min_value=2, max_value=5).map(lambda x: tuple([x, x + 1])),
    ).filter(
        lambda x: "float16" not in x[0]
        and "bfloat16" not in x[0]
        and np.linalg.cond(x[1][0][:, :-1]) < 1 / sys.float_info.epsilon
        and np.linalg.det(x[1][0][:, :-1]) != 0
        and np.linalg.cond(x[1][0][:, -1].reshape(-1, 1)) < 1 / sys.float_info.epsilon
    ),
)
def test_torch_solve(
    *,
    dtype_and_data,
    as_variable,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    with_out,
    frontend,
):
    input_dtype, data = dtype_and_data
    input = data[0][:, :-1]
    other = data[0][:, -1].reshape(-1, 1)
    helpers.test_frontend_function(
        input_dtypes=[input_dtype[0], input_dtype[0]],
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=input,
        other=other,
    )


# eigvals
@handle_frontend_test(
    fn_tree="torch.linalg.eigvals",
    dtype_x=_get_dtype_and_square_matrix(),
)
def test_torch_eigvals(
    *,
    dtype_x,
    num_positional_args,
    as_variable,
    native_array,
    frontend,
    fn_tree,
    on_device,
):
    input_dtype, x = dtype_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
    )
