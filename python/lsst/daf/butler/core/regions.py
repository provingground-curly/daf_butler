# This file is part of daf_butler.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ("makeBoxWcsRegion", )

import lsst.sphgeom
import lsst.geom


def makeBoxWcsRegion(box, wcs, margin):
    """Construct a spherical ConvexPolygon from a WCS and a bounding box.

    Parameters
    ----------
    box : `lsst.geom.Box2I` or `lsst.geom.Box2D`
        A box in the pixel coordinate system defined by the WCS.
    wcs : `lsst.afw.image.Wcs`
        A mapping from a pixel coordinate system to the sky.
    margin : `float`
        A buffer in pixels to grow the box by (in all directions) before
        transforming it to sky coordinates.

    Returns
    -------
    polygon : `lsst.sphgeom.ConvexPolygon`
        A convex polygon.
    """
    box = lsst.geom.Box2D(box)
    box.grow(margin)
    vertices = []
    for point in box.getCorners():
        coord = wcs.pixelToSky(point)
        lonlat = lsst.sphgeom.LonLat.fromRadians(coord.getRa().asRadians(),
                                                 coord.getDec().asRadians())
        vertices.append(lsst.sphgeom.UnitVector3d(lonlat))
    return lsst.sphgeom.ConvexPolygon(vertices)
